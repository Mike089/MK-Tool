# coding=utf-8
import soundcloud
import facebook

print ("CAUTION! IF YOU DONT HAVE A VALID ACCESS-TOKEN FOR THE FACEBOOK A.P.I., YOUR SET WILL GET UPLOADED ON SOUNDCLOUD ANYWAY!")
un = raw_input("Soundcloud Username/E-Mail adress?")
pw = raw_input("Password for Soundloud?")
starttoken = raw_input("Please visit https://developers.facebook.com to get an valid Accesstoken for MKTool. "
                      "Insert Token here:")
path = raw_input("Please insert the correct path to your Set!!")
name = raw_input("Title of your set?")
beschreibung = raw_input("Any description for your set?")
ueberschrift = raw_input("Title for the post on your Fan-Page?")

client = soundcloud.Client(client_id="YOUR_CLIENT_ID",
                           client_secret="YOUR_CLIENT_SECRET",
                           username=un,
                           password=pw)
print ('****ARTIST****')
# Displays your Name
print (client.get("/me").username)


print ('#####RELEASED SETS#####')
# Display already posted sets
tracks = client.get("/tracks", q="Michael Keimenberg", limit=15)
for track in tracks:
    print (track.title)
app = client.get("/apps/124")



print ('+++SET WIRD GEPOSTET.....+++')
print ('Bitte warten.....')


# Set gets uploaded.....(to Soundcloud)
track = client.post("/tracks", track={
    "title": name,
    "sharing": 'public',
    "asset_data": open(path, "rb")
})


# URL des Tracks fuer die Facebookapi
print ('-----URL OF THE SET ON SOUNDCLOUD-----')
fb_url = track.permalink_url
print (fb_url)



app_id = "YOUR_FACEBOOK_APP_ID"
app_secret = "YOUR_FACEBOOK_APP_SECRET"
token = starttoken
graph = facebook.GraphAPI(token)
profile = graph.get_object("MichaelKeimenberg")
posts = graph.get_connections(profile['id'], "posts")

redirect_client_url = 'http://your-redirect-url'
access_token_url = 'https://graph.facebook.com/oauth/acess_token?client_id=' + app_id + '&redirect_uri=' + redirect_client_url + '&client_secret=' + app_secret + '&code='
scope = 'publish_stream,offline_access,user_birthday,email'
authorize_url = 'https://graph.facebook.com/oauth/authorize?client_id=' + app_id + '&redirect_uri=' + redirect_client_url + '&scope=' + scope + 'display=touch'
user_info_url = 'https://graph.facebook.com/me?access_token='

# Post the link of the soundcloud-set to your FB-Page
attachment = {
    'name': name,
    'link': fb_url,
    'caption': 'New set!!',
    'description': beschreibung,
    'picture': 'https://i1.sndcdn.com/avatars-000230326453-yl2mpg-t500x500.jpg'
}

graph.put_wall_post(message=ueberschrift, attachment=attachment)
