import soundcloud
import sys

# Set default encoding
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    # User input for Soundcloud
    sc_login = raw_input('Soundcloud Login: ')
    sc_passwd = raw_input('Soundcloud Password: ')
    fb_token = raw_input('FB access token (visit https://developers.facebook.com): ')
    sc_path = raw_input('Path to audio file: ')
    name = raw_input('Name of your Set: ')
    description = raw_input('Set description: ')
    title = raw_input('Title of post:')

    # Instantiate Soundcloud class
    sc = Soundcloud(sc_login, sc_passwd, sc_path, name)

    # Print Artist name
    print('Artist: {0}'.format(sc.artist))

    # Loop through released tracks
    for track in sc.tracks:
        print('Track: {0}'.format(track.title))

    # Uploads set with sharing 'private'
    sc.upload_set('private')

    fb = Facebook(fb_token);
    fb.post(sc.set.permalink_url, name, description, title)

class Soundcloud:
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'

    def __init__(self, login, passwd, path, name):
        if login is not None and passwd is not None and path is not None and name is not None:
            self.login = login
            self.passwd = passwd
            # TODO: verify if path is valid otherwise raise exeption
            self.path = path
            self.name = name

            # Catch Exception on soundlcoud.Client and exit if fails
            try:
                self.client = soundcloud.Client(client_id=self.client_id, client_secret=self.client_secret, username=login, password=passwd)
                self.get_artist()
                self.get_released_sets()
            except Exception as e:
                print 'Error:',e
                sys.exit(0)
        else:
            # Raises ValueError if user input is empty
            raise ValueError('Soundcloud Login and Password can\'t be empty!')

    # Assigns artists name to Soundcloud property
    def get_artist(self):
        self.artist = self.client.get('/me').username

    # Assigns released tracks to Soundcloud property
    def get_released_sets(self):
        self.tracks = self.client.get('/tracks', q=self.artist, limit=15)

    def upload_set(self, sharing):
        print('+++ Set is beeing uploaded +++')
        # TODO: Implement error handling for file open
        self.set = self.client.post('/tracks', track={'title': self.name, 'sharing': sharing, 'asset_data': open(self.path, 'rb')})
        print('Set URL:', self.set.permalink_url)

class Facebook:
    app_id = 'YOUR_FACEBOOK_APP_ID'
    app_secret = 'YOUR_FACEBOOK_APP_SECRET'

    # TODO: Clean not used code
    def __init__(self, token):
        if token is not None:
            self.token = token
            self.graph = facebook.GraphAPI(self.token)
            self.profile = self.graph.get_object('MichaelKeimenberg')
            self.posts = self.graph.get_connections(profile['id'], 'posts')
            self.redirect_client_url = 'http://your-redirect-url'
            self.access_token_url = 'https://graph.facebook.com/oauth/acess_token?client_id=' + self.app_id + '&redirect_uri=' + self.redirect_client_url + '&client_secret=' + self.app_secret + '&code='
            self.scope = 'publish_stream,offline_access,user_birthday,email'
            self.authorize_url = 'https://graph.facebook.com/oauth/authorize?client_id=' + self.app_id + '&redirect_uri=' + self.redirect_client_url + '&scope=' + self.scope + 'display=touch'
            self.user_info_url = 'https://graph.facebook.com/me?access_token='
        else:
            raise ValueError('Access Token can\'t be empty!')

    def post(self, set_url, name, description, title):
        print('Posting to Facebook wall')
        attachment = {
            'name': name,
            'link': fb_url,
            'caption': 'New set!!',
            'description': description,
            'picture': 'https://i1.sndcdn.com/avatars-000230326453-yl2mpg-t500x500.jpg'
        }
        self.graph.put_wall_post(message=title, attachment=attachment)

# Start
init()
