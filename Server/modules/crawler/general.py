import os

# Each website you crawl is a separate project (folder)

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating Directory' + directory)
        os.makedirs(directory)

# create queue and crawled files ( if not created )
def write_file(path, data):
    f = open(path,'w')
    f.write(data)
    f.close()


def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# Add data onto an exsisting file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data+ '\n')

# Delete the contents of the file
def delete_file_contents(path):
    with open(path, 'w'):
        pass