Help ()
{
  echo "USAGE: "
  echo "------ "
  echo "--> $0 -h (this help)"
  echo "--> $0 <DIRECTORY OF IMAGES> <DIRECTORY TO CREATE IMAGE GALLERY IN>"

}

if [ $# -eq 0 ]; then
    >&2 Help 
    exit 1
fi
while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done
echo "Creating the HTML Gallery from images in: $1";
echo "Gallery being created in: $2";

#export PHOTO_DIR=$1
#export OUTPUT_DIR=$2

# The "-c txt" is actually passed into the container and onto the
# "entrypoint" executable fgallery as it's commandline arguments
# so if you want to modify arguments to fgallery, do it there.
# 
# In this case we use "-c txt" but fgallery can do "-c cmt" 
# which tells fgallery to use a neat feature it has
# which is to pull comment exif data out of the image files
# and use it as text annotation in the generated gallery.
docker run -it -v $1:/photos -v $2:/output sa7ori/bookmark2screenshot_gallerymaker -c txt /photos /output/gallery
