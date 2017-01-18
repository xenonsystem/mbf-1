# Mbf, the mud bot framework - timer class
# Author: Blake Oliver <oliver22213@me.com>

class Timer(object):
	def __init__(self, scheduler, type=None, enabled=True, name=None, group='all', one_shot=False, *args, **kwargs):
		"""Class that wraps an 'APScheduler' job into a timer instance for mbf.
		
		Args:
			scheduler: A reffrence to a scheduler object so a job can be added.
				This should be automatically provided by mbf's 'timer' method, so you shouldn't need to worry about this.
			type: the type of apscheduler trigger that this job or "timer" should use.
				Can be one of 'interval', 'date', or 'cron'.
			enabled: If this timer should be enabled when created. If set to false, it will immediately be paused.
			name: The name of this timer. Set to none by default, the 'timer' decorator will set this to the name of the decorated function. If this particular function will be run by more than one timer, customize this for each one.
				This is actually apscheduler's 'id' attribute, but I've renamed it name because it's more in line with what triggers use.
			group: The group that this timer instance belongs to. Set to 'all' by default
			one_shot: Specifies that this timer should run only once, and then be removed. If the type arg is set to 'date', one_shot is implicitly true.
		Any extra args and keyword args are passed to APScheduler's 'create_job' method. 
		"""
		self.scheduler = scheduler
		self.type = type
		self._enabled = enabled
		self.name = name
		self.group = group
		self.one_shot = one_shot
		self.fn = None
		self.job = self.scheduler.add_job(self.fire, self.type, *args, **kwargs)
	
	def fire(self, *function_args, **function_kwargs):
		"""This method is what each APScheduler job actually 'fires';
			For now, it simply calls the associated function for the timer instance (self.fn).
		To specify args and kwargs for the timer's associated function to run, add 'args' and 'kwargs', items, of types list and dict (respectively) to mbf's timer decorator or on 'Timer' class initialization; they'll get passed to add_job which will pass them to this method.
		"""		
		if self.fn is not None:
			self.fn(*function_args, **function_kwargs)
		else:
			# throw a specific exception here that has yet to be created
			pass
	
	@property
	def enabled(self):
		return self._enabled
	
	@enabled.setter
	def enabled(self, val):
		"""Enable this timer / job"""
		if job is not None and val != self._enabled:
			if val == True:
				self._enabled = True
				self.job.resume()
			elif val == False:
				self._enabled = False
				self.job.pause()
	
	def enable(self):
		self.enabled = True
	
	def disable(self):
		self.enabled = False
	
	def add_function(self, f):
		"""Associate a function to get run when this timer fires
		The function can accept any number of arguments and keyword arguments; the timer class doesn't impose any restrictions or expect it to receive any arguments.
		"""
		self.fn = f
