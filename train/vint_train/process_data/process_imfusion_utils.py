import imfusion
import argparse

import pickle as pkl
import os
from pyquaternion import Quaternion


def load_imf_us(file_path):

    return_list = []

    imfusion_data = imfusion.load(file_path)
    if (len(imfusion_data) == 0):
        print("File: ", imfusion_data, " empty")
        return []
    
    for us in imfusion_data:
        if not isinstance(us, imfusion.TrackedSharedImageSet):
            continue
        return_list.append(us)  
        

    return return_list 
        
   


def get_images_and_trajectories(
    imfusion_data,
    config
):
    """
    Get image and odom data from a bag file

    Args:
        bag (rosbag.Bag): bag file
        imtopics (list[str] or str): topic name(s) for image data
        odomtopics (list[str] or str): topic name(s) for odom data
        img_process_func (Any): function to process image data
        odom_process_func (Any): function to process odom data
        rate (float, optional): rate to sample data. Defaults to 4.0.
        ang_offset (float, optional): angle offset to add to odom data. Defaults to 0.0.
    Returns:
        img_data (list): list of PIL images
        traj_data (list): list of odom data
    """

    imfusion_data = imfusion.load(imfusion_file_path)
        
    if (len(imfusion_data) == 0):
        print("File: ", imfusion_data, " empty")
        return [], []
        
        
    for us in imfusion_data:
        if not isinstance(us, imfusion.TrackedSharedImageSet):
            continue
        traj = extract_trajectory_from_file()




    # check if bag has both topics
    odomtopic = None
    imtopic = None
    if type(imtopics) == str:
        imtopic = imtopics
    else:
        for imt in imtopics:
            if bag.get_message_count(imt) > 0:
                imtopic = imt
                break
    if type(odomtopics) == str:
        odomtopic = odomtopics
    else:
        for ot in odomtopics:
            if bag.get_message_count(ot) > 0:
                odomtopic = ot
                break
    if not (imtopic and odomtopic):
        # bag doesn't have both topics
        return None, None

    synced_imdata = []
    synced_odomdata = []
    # get start time of bag in seconds
    currtime = bag.get_start_time()

    curr_imdata = None
    curr_odomdata = None

    for topic, msg, t in bag.read_messages(topics=[imtopic, odomtopic]):
        if topic == imtopic:
            curr_imdata = msg
        elif topic == odomtopic:
            curr_odomdata = msg
        if (t.to_sec() - currtime) >= 1.0 / rate:
            if curr_imdata is not None and curr_odomdata is not None:
                synced_imdata.append(curr_imdata)
                synced_odomdata.append(curr_odomdata)
                currtime = t.to_sec()

    img_data = process_images(synced_imdata, img_process_func)
    traj_data = process_odom(
        synced_odomdata,
        odom_process_func,
        ang_offset=ang_offset,
    )

    return img_data, traj_data








def find_imf_files(root_folder):
    imf_files = []

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.imf'):
                absolute_path = os.path.abspath(os.path.join(dirpath, filename))
                imf_files.append(absolute_path)
    
    return imf_files

def get_file_paths(folder_path):
    
    # TODO: return the list of file paths
    return []


def save_to_pkl(file_path, file_content):
    pkl.dump(file_content, file_path)

def extract_trajectory_from_file(trackedImage : imfusion.TrackedSharedImageSet):
    
    for i in range(trackedImage.size()):
        mat = trackedImage.matrix()
    return None


def run(input_folder):
    imf_files = find_imf_files(input_folder)
    for item in imf_files:
        imfusion_data = imfusion.load(item)
        
        if (len(imfusion_data) == 0):
            print("File: ", item, " empty")
            continue
        
        data = imfusion.Data()
        data.kind
        for us in imfusion_data:
            if not isinstance(us, imfusion.TrackedSharedImageSet):
                continue
            traj = extract_trajectory_from_file()
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple example script.")
    
    # Adding arguments
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to the input folder'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Path to the output folder'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Increase output verbosity'
    )

    args = parser.parse_args()
    