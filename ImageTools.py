import imghdr

# Image Paths
def get_image_paths_from_folders(self, folders):
    images = []
    for folder in folders:
        images.extend(self.get_image_paths_from_folder(folder))
    return images


def get_image_paths_from_folder(self, folder):
    results = []
    for file in os.listdir(folder):
        try:
            if imghdr.what(folder + file):
                results.append(str(folder + file).replace('\\', '/').replace('\\', '/'))
        except(PermissionError):
            if self.debug:
                print('Permission to Subfolder denied')
    return results