import asyncio

from src.exceptions import BaseException

class Pipes(list):
   def __init__(self, pipes=None):
      super().__init__(pipes or [])

   def add_all(self, pipes):
      self.extend(pipes)

class Pipeline:
   def __init__(self, pipes=None):
      self.pipes = pipes or Pipes()
      self.passed = []

   def add(self, method):
      if isinstance(method, (list, Pipes)):
         new_pipeline = Pipeline(method)
         self.pipes.append(lambda: new_pipeline.run())
      elif isinstance(method, (Pipeline, Recurrence)):
         self.pipes.append(lambda: method.run(self))
      else:
         self.pipes.append(method)

   def add_all(self, methods):
      for method in methods:
         self.add(method)

   async def run(self):
      for method in self.pipes:
         try:
            await method()
            self.passed.append(True)
         except Exception as error:
            self.passed.append(False)
            BaseException.raise_exc(error)

class Recurrence:
   def __init__(self, delay=500):
      self.delay = delay
      self.pipeline: Pipeline = None

   async def run(self, pipeline: Pipeline):
      await asyncio.sleep(self.delay / 1000)
      self.pipeline: Pipeline = pipeline
      await self.pipeline.run()

