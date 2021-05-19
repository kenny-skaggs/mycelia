from google.cloud import ndb


class Settings:
    name = ndb.StringProperty()
    value = ndb.StringProperty()

    @classmethod
    def get(cls, name):
        _EnvSettings.get(name)


class DatastoreSettings:
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatastoreSettings, cls).__new__(cls)
            cls._instance.unset_value = 'VALUE_NOT_YET_SET'
            cls._instance.client = ndb.Client()
        return cls._instance

    @classmethod
    def get(cls, name):
        instance = DatastoreSettings()
        with instance.client.context():
            setting = _DataStoreRecord.query(_DataStoreRecord.name == name).get()
            if not setting:
                setting = _DataStoreRecord(name=name, value=instance.unset_value)
                setting.put()

            if setting.value == instance.unset_value:
                raise Exception(f'Value for setting "{name}" has not been set yet.')

            return setting.value


class _DataStoreRecord(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()


class _EnvSettings:
    @classmethod
    def get(cls, name):
        return name
