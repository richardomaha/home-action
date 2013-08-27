#!/usr/bin/env python

# 1 - wget http://linux-metrics.googlecode.com/files/linux-metrics-0.1.2.tar.gz
# 2 - tar -zxvf linux-metrics-0.1.2.tar.gz
# 3 - cd linux-metrics-0.1.2/
# 4 - python setup.py install
# 5 - rm linux-metrics-0.1.2.tar.gz
#   - rm -Rf linux-metrics-0.1.2

import linux_metrics as lm

class Monitor:
	def __init__(self):
		self.processors = 1
		self.cpu_usage = 0
		self.memory_used = 0
		self.memory_total = 0
		self.memory_usage = 0
		
	def cpu(self):
		self.processors =  lm.cpu_stat.procs_running()
		cpu_pcts = lm.cpu_stat.cpu_percents(sample_duration=1)
		#print 'cpu utilization: %.2f%%' % (100 - cpu_pcts['idle'])
		self.cpu_usage = 100-cpu_pcts['idle']

	def memory(self):
		used, total = lm.mem_stat.mem_stats()
		self.memory_used =  used
		self.memory_total = total
		self.memory_usage = (float(used)/float(total))

	def stats_to_xml(self):
		xml = """
		<device>
			<processors>%d</processors>
			<cpu_usage>%f</cpu_usage>
			<memory_used>%d</memory_used>
			<memory_total>%d</memory_total>
			<memory_usage>%f</memory_usage>
		</device>
		""" % (self.processors, self.cpu_usage, self.memory_used, self.memory_total, self.memory_usage)
		return xml
