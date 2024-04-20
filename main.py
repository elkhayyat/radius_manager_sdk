from api import RMClient
from models.users import User

rm = RMClient('localhost', 'api', 'api123')

user = User(username='admin', password='admin')
u = rm.create_user(**user.data_in_rm_format)
input('Press Enter to delete the user...')
rm.delete_user('admin')
