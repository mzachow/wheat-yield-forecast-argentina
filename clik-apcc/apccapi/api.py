import json
import time
import os
import requests
import logging
import urllib3


def read_config(path):
	config = {}
	with open(path) as f:
		for l in f.readlines():
			if '=' in l:
				k, v = l.strip().split('=')	
				if k in ('request_url', 'key', 'status_url'):
					config[k] = v.strip()
	return config


class Client(object):

	logger = logging.getLogger('apccapi')

	def __init__(self, 
				debug=False,
				sleep_max=120,
				retry_max=500,
				timeout=60):
		
		self.sleep_max = sleep_max
		self.retry_max = retry_max
		self.timeout = timeout
		self.last_status = None
		self.target = None

		if debug:
			level = logging.DEBUG
		else:
			level = logging.INFO

		logging.basicConfig(level=level, 
			format='[%(asctime)s] [%(levelname)s] %(message)s')	

		self.requesturl = None
		self.key = None
		self.statusurl = None

		urllib3.disable_warnings()

		propertyFile = 'C:/Users/Max Zachow/apccapi.properties'
		self.debug(propertyFile)

		if self.requesturl is None or self.key is None or self.statusurl is None:
			if os.path.exists(propertyFile):
				config = read_config(propertyFile)

				self.key = config.get('key')
				self.requesturl = config.get('request_url')
				self.statusurl = config.get('status_url')

		if self.requesturl is None or self.key is None or self.statusurl is None:
			raise Exception('Missing/incomplete properties file: %s' % (propertyFile))

	
	def retrieve(self, details, target):

		headers = {'Content-Type': 'application/json; charset-utf-8'}
		request = {}
		request['key'] = self.key
		request['details'] = details

		self.target = target

		try:
			response = self.post_api(self.requesturl, request)
			print(response)
			reply = response.json()
			status_code = reply['status']
			message = reply['message']
		except Exception:
#			self.debug(response.text)
			raise
	
		if status_code > 202:
			info = reply['data']['info']
			self.error(message + "-" + info)
			return None

	
		sleep = 0
		jobid = None

		while True:

			self.debug("REPLY %s", reply)

			if sleep == 0:
				jobid = reply['data']['id']
				userid = reply['data']['userid']
				self.info('Hello ' + userid + ".")
				self.info('Your job id is ' + jobid)
			
			if reply['data']['status'] != self.last_status:
				self.info("Request is %s" % (reply['data']['status'],))
				self.last_status = reply['data']['status']
		
			if reply['data']['status'] == 'Complete':
				self.debug("Done")
				result = self.download(reply['data']['download_url'], self.target)
				if result is False:
					self.error('Failed to download result file.')

				return

			if reply['data']['status'] == 'Queued' or reply['data']['status'] == 'Running':
				self.debug("Request ID is %s, sleep %s", jobid, sleep)
				time.sleep(3)
				sleep += 3;

				if sleep > self.sleep_max:
					sleep = self.sleep_max

				status_url = '%s/%s' % (self.statusurl, jobid)
				self.debug("GET %s", status_url)

				try:
					response = self.get_api(status_url)
					reply = response.json()
				except Exception:
					self.debug("Failed to get response. Retrying");	

				continue

			if reply['data']['status'] == "Failed":
				print(reply['data']['message'])
				return

			raise Exception('Unknown API state [%s]' % reply['data']['status'])


	def download(self, url, target):

		self.info('Start to save file - ' + target)

		tries = 0

		while tries < self.retry_max:
			try:
				response = requests.get(url, verify=False, allow_redirects=True)
				open(target, 'wb').write(response.content)
			except requests.exceptions.ConnectionError as e:
				self.warning("Recovering from connection error [%s], attemps %s of %s",
					response.status_code, response.reason, tries, self.retry_max)

			if os.path.exists(target):
				self.info('Done')
				return True

			tries += 1

			self.warning("Retrying in %s seconds", self.sleep_max)
			time.sleep(self.sleep_max)
			self.info("Retrying now...")

		return False


	def get_api(self, url):

		tries = 0

		while tries < self.retry_max:
			try:
				response = requests.get(url, verify=False)
			except requests.exceptions.ConnectionError as e:
				response = None
				self.warning("Recovering from connection error [%s], attemps %s of %s",
							response.status_code, response.reason, tries, self.retry_max)

			if response	is not None:
				if response.status_code == 202 or response.status_code == 200:
					return response
				else:
					self.error('Failed to get status of the job.')
					#self.error(status_json['data']['info'])

			tries += 1

			self.warning("Retrying in %s seconds", self.sleep_max)
			time.sleep(self.sleep_max)
			self.info("Retrying now...")

		return None


	def post_api(self, url, request):

		headers = {'Content-Type': 'application/json; charset-utf-8'}	
		tries = 0

		while tries < self.retry_max:
			try:
				response = requests.post(url, verify=False, headers=headers, data=json.dumps(request))
			except requests.exceptions.ConnectionError as e:
				response = None
				self.warning("Recovering from connection error [%s], attemps %s of %s",
							 e, tries, self.retry_max)

			if response	is not None:
				if response.status_code > 202:
					self.warning("Recovering from HTTP error [%s %s], attemps %s of %s",
							response.status_code, response.reason, tries, self.retry_max)
			
				else:
					return response				


			tries += 1

			self.warning("Retrying in %s seconds", self.sleep_max)
			time.sleep(self.sleep_max)
			self.info("Retrying now...")

		return None


	def info(self, *args, **kwargs):
		self.logger.info(*args, **kwargs)

	def warning(self, *args, **kwargs):
		self.logger.warning(*args, **kwargs)

	def error(self, *args, **kwargs):
		self.logger.error(*args, **kwargs)

	def debug(self, *args, **kwargs):
		self.logger.debug(*args, **kwargs)

