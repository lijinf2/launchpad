# Copyright 2020 DeepMind Technologies Limited. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example presents clean node termination."""



import time

from absl import app
from absl import logging
import launchpad as lp



def _sleep():
  try:
    while True:
      time.sleep(1)
  except SystemExit:
    logging.info('Clean termination of _sleep node')
    time.sleep(2)


def _wait_for_stop():
  lp.wait_for_stop()
  logging.info('Clean termination of _wait_for_stop node')
  time.sleep(2)


def _infinite_sleep():
  # Sleep call can't be interrupted outside of the main thread, so in local_mt
  # mode for instance this node will be hard-killed.
  try:
    time.sleep(1000000)
  except SystemExit:
    logging.info('Clean termination of _infinite_sleep node')
    time.sleep(2)


def _stop_program():
  time.sleep(2)
  lp.stop()


def make_program() -> lp.Program:
  """Define the distributed program topology."""
  program = lp.Program('program_wait')
  program.add_node(lp.CourierNode(_sleep), label='sleep')
  program.add_node(lp.CourierNode(_wait_for_stop), label='_wait_for_stop')
  program.add_node(lp.CourierNode(_infinite_sleep), label='_infinite_sleep')
  program.add_node(lp.CourierNode(_stop_program), label='_stop_program')
  return program


def main(_):
  program = make_program()

  lp.launch(program)  


if __name__ == '__main__':
  app.run(main)
