from json_log_formatter import JSONFormatter

class CustomJSONFormatter(JSONFormatter):
    def json_record(self, message, extra, record):
        extra['timestamp'] = self.formatTime(record)
        extra['level'] = record.levelname
        extra['message'] = message
        extra['module'] = record.module
        return extra

