import re

def get_user_title(result):
    p = re.search("title(.*?)\]\,", str(result))
    title = re.sub(r'title\': \[b\'', "", p[0])
    title = re.sub(r'\']\,', "", title)
    return title
# returns user's full_name
def get_user_fullname(result):
    p = re.search("displayName(.*?)\]\,", str(result))
    full_name = re.sub(r'displayName\': \[b\'', "", p[0])
    full_name = re.sub(r'\/.*', "", full_name)
    name = full_name.split(", ")[1] + " " + full_name.split(", ")[0]
    return name
# checks whether user is in GRP_SKI_Haystack_NetIQ
# returns ezGroups the user is a part of
def get_user_group(result):
    # compiles reg ex pattern into reg ex object
    p = re.compile('CN=(.*?)\,')
    groups = re.sub('CN=Users', '', str(result))
    print(groups)
    # returns all matching groups
    return p.findall(groups)

