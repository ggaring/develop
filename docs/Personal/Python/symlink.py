#!/usr/bin/python3
import os
import shutil

Deployment_dir = '/home/ggaring/Desktop/Personal/test-env-folder'


def remove_unused_tarbals(PATH):
    active_tarballs = []
    inactive_tarballs = []

    for tarball in os.listdir(PATH):
        tarball = os.path.join(PATH, tarball)
        #to check if it's an active dir
        if os.path.islink(tarball):
            print('{} is an active tarball'.format(tarball))
            active_tarballs.append(os.path.realpath(tarball))
        elif os.path.isdir(tarball):
            inactive_tarballs.append(tarball)
    print(active_tarballs)
    print(inactive_tarballs)

    inactive_tarballs = set(inactive_tarballs) - set(active_tarballs)
    print("About to remove {}".format(inactive_tarballs))
    for inactive_tarball in inactive_tarballs:
        print("Removing {}".format(inactive_tarball))
        shutil.rmtree(inactive_tarball)

    for active_tarball in active_tarballs:
        print("Keeping {}".format(active_tarball))

if __name__ == '__main__':
        print("Cleaning up old tarballs")
        remove_unused_tarbals(Deployment_dir)
