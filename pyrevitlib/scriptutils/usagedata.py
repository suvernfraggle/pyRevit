# import os
# import os.path as op
# import shutil as shutil
# from datetime import datetime
#
# from pyrevit import PYREVIT_ADDON_NAME, PyRevitException
# from pyrevit.coreutils.logger import get_logger
# from pyrevit.coreutils.appdata import PYREVIT_APP_DIR
# from pyrevit.userconfig import user_config
#
# # noinspection PyUnresolvedReferences
# from System.Diagnostics import Process
# # noinspection PyUnresolvedReferences
# from System.IO import IOException
#
#
# logger = get_logger(__name__)
#
#
# LOG_FILE_TYPE = 'log'
# LOG_ENTRY_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
#
#
# # todo: add resolution to usage data tool. Some tools are used within close timing to each other.
#
# def archive_script_usage_logs():
#     """Archives older script usage log files to the folder provided by user in user settings.
#     :return: None
#     """
#     if op.exists(user_config.core.archivelogfolder):
#         host_instances = list(Process.GetProcessesByName('Revit'))
#         if len(host_instances) > 1:
#             logger.debug('Multiple Revit instance are running...Skipping archiving old log files.')
#         elif len(host_instances) == 1:
#             logger.debug('Archiving old log files...')
#             files = os.listdir(PYREVIT_APP_DIR)
#             for f in files:
#                 if f.startswith(PYREVIT_ADDON_NAME) and f.endswith(LOG_FILE_TYPE):
#                     try:
#                         current_file_path = op.join(PYREVIT_APP_DIR, f)
#                         newloc = op.join(user_config.core.archivelogfolder, f)
#                         shutil.move(current_file_path, newloc)
#                         logger.debug('Existing log file archived to: {}'.format(newloc))
#                     except IOException as io_err:
#                         logger.warning('Error archiving log file: {} | {}'.format(f, io_err.Message))
#                     except Exception as err:
#                         logger.warning('Error archiving log file: {} | {}'.format(f, err))
#     else:
#         logger.debug('Archive log folder does not exist: {}. Skipping...'.format(user_config.core.archivelogfolder))
#
#
# # script usage database interface ---------------------------------------------------------------------------------
# class UsageDataEntry:
#     """Database entry object."""
#
#     def __init__(self, log_entry):
#         """Initialize by a log file entry string.
#         Sample log entry:
#         2016-10-25 10:51:20, eirannejad, 2016, L:\pyRevitv3\pyRevit\pyRevit.tab\Select_addTaggedElementsToSelection.py
#         :param str log_entry:
#         """
#         try:
#             # extract main components
#             time_date, self.user_name, self.host_version, self.script_entry = log_entry.split(',', 3)
#
#             # extract datetime
#             self.usage_datetime = datetime.strptime(time_date, LOG_ENTRY_DATETIME_FORMAT)
#
#             # extract script directory and name
#             # todo: proper script name extraction for new and legacy scripts
#             self.script_directory = op.dirname(self.script_entry)
#             self.script_name = op.basename(self.script_entry)
#         except Exception as err:
#             raise PyRevitException('Error creating entry from string: {} | {}'.format(log_entry, err))
#
#
# # Create interface???????? per PEP249 standard: https://www.python.org/dev/peps/pep-0249/
# class UsageDatabase:
#     def __init__(self):
#         self._db = []           # list of UsageDataEntry objects
#         self.files_processed = 0
#         self._read_log_files(PYREVIT_APP_DIR)
#         self._read_log_files(user_config.core.archivelogfolder)
#
#     def __iter__(self):
#         return iter(self._db)
#
#     # data init functions ------------------------------------------------------------------------------------------
#     @staticmethod
#     def _verify_log_file(file_name):
#         """
#         :param str file_name:
#         :return: bool
#         """
#         return PYREVIT_ADDON_NAME.lower() in file_name.lower() and file_name.endswith(LOG_FILE_TYPE)
#
#     def _read_log_files(self, log_dir):
#         """find all log files in log_dir and reads them line by line and creates database entries
#         :param str log_dir:
#         :return: None
#         """
#         logger.debug('Reading log files in: {}'.format(log_dir))
#         for parsed_file in os.listdir(log_dir):
#             if self._verify_log_file(parsed_file):
#                 full_log_file = op.join(log_dir, parsed_file)
#                 logger.debug('Reading log file: {}'.format(full_log_file))
#                 with open(full_log_file, 'r') as log_file:
#                     self.files_processed += 1
#                     for line_no, log_entry in enumerate(log_file.read().splitlines()):
#                         try:
#                             self._db.append(UsageDataEntry(log_entry))
#                         except PyRevitException as err:
#                             logger.debug('Error creating entry (Line No/Log file): {}/{} | {}'.format(line_no,
#                                                                                                       full_log_file,
#                                                                                                       err))
#
#     # data query functions ----------------------------------------------------------------------------------------
#     def get_usernames(self):
#         unames = set()
#         for entry in self:  # type: UsageDataEntry
#             unames.add(entry.user_name)
#         return list(unames)
#
#     def get_scripts(self):
#         scripts = set()
#         for entry in self:  # type: UsageDataEntry
#             if entry.script_name != 'script.py':
#                 scripts.add(entry.script_name)
#
#         return list(scripts)
#
#     def get_script_usage_count(self, script_name):
#         count = 0
#         for entry in self:  # type: UsageDataEntry
#             if entry.script_name == script_name:
#                 count += 1
#         return count
#
#
# def get_usagedata_db():
#     """Returns an instance of the usagedata database
#     :return: UsageDatabase
#     """
#     return UsageDatabase()
