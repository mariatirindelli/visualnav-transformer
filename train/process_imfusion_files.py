import os
import pickle
import yaml

# utils
from vint_train.process_data.process_imfusion_utils import *

def main(args: argparse.Namespace):

    # load the config file
    if os.path.exists("vint_train_imfusion/process_data/process_bags_config.yaml"):
        with open("vint_train_imfusion/process_data/process_bags_config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    else:
        config = None

    # create output dir if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # iterate recurisively through all the folders and get the path of files with .bag extension in the args.input_dir
    imfusion_files = []
    for root, _, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith(".imf"):
                imfusion_files.append(os.path.join(root, file))

        # TODO: remove this
        if len(imfusion_files) > 10:
            break

    #if args.num_trajs >= 0:
    #    imfusion_files = imfusion_files[: args.num_trajs]


    counter = 0
    # processing loop
    for imfusion_file in imfusion_files:

        for (i, data) in enumerate(load_imf_us(imfusion_file)):
        
            # name is that folders separated by _ and then the last part of the path
            traj_name = "_".join(imfusion_file.split("/")[-2:])[:-4] + str(i)

            # load the hdf5 file
            imfusion_img_data, imfusion_traj_data = get_images_and_trajectories(
               data,
               config
            )

            # TODO: understand what to add to filter backwards
            # cut_trajs = filter_backwards(bag_img_data, bag_traj_data) # remove backwards movement

            cut_trajs = zip(imfusion_img_data, imfusion_traj_data)

            for i, (img_data_i, traj_data_i) in enumerate(cut_trajs):
                traj_name_i = traj_name + f"_{i}"
                traj_folder_i = os.path.join(args.output_dir, traj_name_i)
                # make a folder for the traj
                if not os.path.exists(traj_folder_i):
                    os.makedirs(traj_folder_i)
                with open(os.path.join(traj_folder_i, "traj_data.pkl"), "wb") as f:
                    pickle.dump(traj_data_i, f)
                # save the image data to disk
                for i, img in enumerate(img_data_i):
                    img.save(os.path.join(traj_folder_i, f"{i}.jpg"))

                counter += 1
                if (counter > args.num_trajs):
                    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # get arguments for the recon input dir and the output dir
    # add dataset name
    parser.add_argument(
        "--dataset-name",
        "-d",
        type=str,
        help="name of the dataset (must be in process_config.yaml)",
        default="tartan_drive",
        required=True,
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        type=str,
        help="path of the datasets with imfusion files",
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="../datasets/tartan_drive/",
        type=str,
        help="path for processed dataset (default: ../datasets/tartan_drive/)",
    )
    # number of trajs to process
    parser.add_argument(
        "--num-trajs",
        "-n",
        default=-1,
        type=int,
        help="number of bags to process (default: -1, all)",
    )
    # sampling rate
    parser.add_argument(
        "--sample-rate",
        "-s",
        default=4.0,
        type=float,
        help="sampling rate (default: 4.0 hz)",
    )

    args = parser.parse_args()
    # all caps for the dataset name
    print(f"STARTING PROCESSING {args.dataset_name.upper()} DATASET")
    main(args)
    print(f"FINISHED PROCESSING {args.dataset_name.upper()} DATASET")
