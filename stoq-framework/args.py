#   Copyright 2014-2016 PUNCH Cyber Analytics Group
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""

Overview
========

*StoqArgs()* contains the primary command line arguments for the *stoQ*
Framework. All command line options made available in this function will be
made avilable to plugins that are extended with this function.

.. note:: Command line arguments defined within StoqArgs() will be made
          available globally within the *stoQ* Framework. Plugin command line
          arguments must not be defined here, but should instead be defined
          within the plugin itself.

Examples
========

From within a worker plugin, define command line arguments::

    import sys
    import argparse
    from stoq.args import StoqArgs

    # Instantiate our workers command line argument parser
    parser = argparse.ArgumentParser()

    # Initialize the default requirements for a worker, if needed.
    parser = StoqArgs(parser)

    # Define the argparse group for this plugin
    worker_opts = parser.add_argument_group("Plugin Options")

    # Define the command line arguments for the worker
    worker_opts.add_option("-r", "--rules",
                            dest='rulepath',
                            help="Path to rules file.")

    # The first command line argument is reserved for the framework.
    # The work should only parse everything after the first command
    # line argument. We must always use stoQ's argv object to ensure
    # the plugin is properly instantied whether it is imported or
    # used via a command line script
    options = parser.parse_args(self.stoq.argv[2:])

    # If we need to handle command line argument, let's pass them
    # to super().activate so they can be instantied within the worker
    super().activate(options=options)


This will extend the command line arguments from those made available
at initialization, to those defined in *worker_opts*. The variable
``rulepath``, defined above, will be accessible by calling ``worker.rulepath``

API
===
"""


def StoqArgs(parser):
    """
    Initializes command line arguments within the plugin

    :param parser: argparse object for parsing

    :returns: Modified argparse object

    """

    stoq_opts = parser.add_argument_group('General Options')
    stoq_opts.add_argument("-L", "--loglevel",
                           dest='log_level',
                           default=False,
                           choices=['debug', 'info', 'warning', 'error' 'critical'],
                           help="Log level")
    stoq_opts.add_argument("-T", "--template",
                           dest='template',
                           default=False,
                           help="Name of template to use for output")
    stoq_opts.add_argument("-M", "--max-processes",
                           dest='max_processes',
                           default=False,
                           type=int,
                           help="Max number of processes (if supported by source plugin)")
    stoq_opts.add_argument("-R", "--max_recursion",
                           dest='max_recursion',
                           default=False,
                           type=int,
                           help="Max level for recursion into dispatched payloads")

    conn_opts = parser.add_argument_group('Connector Options')
    conn_opts.add_argument("-C", "--connector",
                           dest='output_connector',
                           default=False,
                           help="Connector plugin for the output of worker results")
    conn_opts.add_argument("-A", "--archive",
                           dest='archive_connector',
                           default=False,
                           help="Connector plugin used to archive files")
    conn_opts.add_argument("-S", "--split",
                           dest='combined_results',
                           action='store_false',
                           help="Split results on a per plugin basis")

    source_opts = parser.add_argument_group('Ingest Options')
    source_opts.add_argument("-F", "--file",
                             dest='path',
                             default=False,
                             help="Filename or directory to use for ingesting")
    source_opts.add_argument("-O", "--outfile",
                             dest='outfile',
                             default=False,
                             help="Filename to save reults to (if applicable)")
    source_opts.add_argument("-I", "--ingest",
                             dest='source_plugin',
                             default=False,
                             help="Source plugin to utilize for ingesting")
    source_opts.add_argument("-E", "--errors",
                             dest='error_queue',
                             default=False,
                             action='store_true',
                             help="Process errors (if applicable)")
    source_opts.add_argument("-D", "--dispatch",
                             dest='dispatch',
                             default=False,
                             action='store_true',
                             help="Use yara to automatically dispatch payloads")
    source_opts.add_argument("--tlp",
                             dest='default_tlp',
                             default=False,
                             choices=['white', 'green', 'amber', 'red'],
                             help="TLP level to tag each payload with")
    source_opts.add_argument("--metadata",
                             dest='ingest_metadata',
                             default=False,
                             nargs='*',
                             metavar=('key:value'),
                             help="Metadata to add to the results (i.e., tag:APT1 submitter:stoq)")
    source_opts.add_argument("--rate-limit",
                             dest='ratelimit',
                             default=False,
                             metavar=('count/seconds'),
                             help="Limit the amount of samples to process per second")

    return parser
