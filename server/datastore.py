from google.cloud import ndb

UNSET = 'VALUE_NOT_YET_SET'
client = ndb.Client()


class Settings(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.StringProperty()

    @classmethod
    def get(cls, name):
        with client.context():
            setting = Settings.query(Settings.name == name).get()
            if not setting:
                setting = Settings(name=name, value=UNSET)
                setting.put()

            if setting.value == UNSET:
                raise Exception(f'Value for setting "{name}" has not been set yet.')

            return setting.value
