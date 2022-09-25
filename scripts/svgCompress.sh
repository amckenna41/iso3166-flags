#!/bin/bash

############################## SVG Compress ##############################
'
SVG files can be quite large in size but a lot of its data can be 
redundant or unncessary information so I created this script to help
maximise the storage of the files, especially since the output folder may
contain thousands of files. The script utilises the scour Python library 
to compress the output SVG files if they meet a specific threshold of 
file size. These files are then copied to the output folder. If file size 
threshold is not met or the file is not an SVG then the original file is 
copied to the output. Any other image file types such as png, jpg or gif
are copied to the output folder.
'
##########################################################################

### check current version of pip and update, if neccessry ###
python3 -m pip install --user --upgrade pip

#Help Funtion showing script usage
Help()
{
   echo "Bash Script for compressing SVG files if they are above certain file size threshold."
   echo ""
   echo "Basic Usage, using default parameters: ./svgCompress.sh "
   echo "Usage: ./svgCompress.sh [--input --output --filesize]"
   echo ""
   echo "Options:"
   echo "-h          help"
   echo "-input      Path to input directory of country flags to compress."
   echo "-output     Path to output directory to store compressed SVG files."
   echo "-filesize   Filesize threshold in KB, if file above it then execute compression algorithm."
   exit
}

#parse all input arguments
for i in "$@"
do
case $i in
    -i=*|--input=*)
    INPUT="${i#*=}"
    shift # past argument=value
    ;;
    -o=*|--output=*)
    OUTPUT="${i#*=}"
    shift # past argument=value
    ;;
    -f=*|--filesize=*)
    FILESIZE_THRESHOLD="${i#*=}"
    shift # past argument=value
    ;;
    -h|--h)
    Help
    shift # past argument=value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument with no value
    ;;
    *)
          # unknown option
    ;;
esac
done

if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 $1
fi

#set default values for input parameters if empty
if [ -z "$INPUT" ]; then
  INPUT="countries/"
fi

if [ -z "$OUTPUT" ]; then
  OUTPUT="outputs/"
fi

if [ -z "$FILESIZE_THRESHOLD" ]; then
  FILESIZE_THRESHOLD=50
fi

#check if input and output dirs exist
[ ! -d "$INPUT" ] && echo "Input directory path does not exist." && exit 1
[ ! -d "$OUTPUT" ] && mkdir $OUTPUT

#calculate output filesize before and after compression script
OUTPUT_FOLDERSIZE_PRE=$(du -sh $INPUT | cut -f1 | rev | cut -c 2- | rev)

#start time of script
start=`date +%s`

echo ""
echo "##############################################"
echo "Compressing SVG Files using scour algorithm..."
echo ""
echo "Input Folder: $INPUT"
echo "Output Folder: $OUTPUT"
echo "Filesize Threshold: $FILESIZE_THRESHOLD KB"
echo ""
echo "#############################################"
echo ""


#iterate through all svg's in dir, compressing if over the KB threshold and copy to output folder
for dir in $INPUT*; do 

  #go to next iteration if current dir == output dir
  if [[ "$dir" == "$OUTPUT" ]]; then
    continue
  fi
  
  #create country name folder in output dir if not already created
  countryFolder="$(basename -- "$dir")/"
  [ ! -d "$OUTPUT/$countryFolder" ] && mkdir "$OUTPUT/$countryFolder"

  echo ""
  echo "##### "$(basename -- "$dir")" #####"
  echo ""

  #iterate through all subfolders and files in input dir, calculate their file size and compress using SVG algorithm
  for file in "$dir"/*; do

    #get basename and extension of file
    bname="$(basename -- "$file")"
    extension="${bname##*.}"

    #output filepath for compressed file
    outputPath="$OUTPUT$countryFolder$bname"

    #if output file already exists then skip to next file
    if [ -f "$OUTPUT$countryFolder$bname" ]; then
      echo "Output file "$OUTPUT$countryFolder$bname" already exists."
      continue
    fi

    #if file type != .svg (is png or jpg) then continue but still copy file to outputs
    if [[ "$extension" != "svg" ]]; then
      cp "$file" "$OUTPUT$countryFolder$bname"
      continue
    fi
    
    #get file size in bytes
    filesize=$(wc -c "$file" | awk '{print $1}')
    #get file size in KB
    filesize=$(expr $filesize / 1024)

    #if file size > threshold, compress SVG using scour library
    if (("$filesize" > "$FILESIZE_THRESHOLD")); then
        scour -i "$file" -o "$OUTPUT$countryFolder$bname" --enable-viewboxing --enable-id-stripping \
        --enable-comment-stripping --shorten-ids --indent=none
    else
        #copy files less than threshold to outputs folder
        cp "$file" "$OUTPUT$countryFolder$bname"
    fi  
      
    done

done

#end time of script
end=`date +%s`
#calculate total runtime
runtime=$((end-start))

#validating correct num files is the same in INPUT and OUTPUT folders
totalInputFolders=0
totalInputFiles=0
totalOutputFolders=0
totalOutputFiles=0

for dir in $INPUT*; do 

    totalInputFolders=$((totalInputFolders+1))

  for file in "$dir"/*; do

    totalInputFiles=$((totalInputFiles+1))

  done

done

for dir in $OUTPUT*; do 

    totalOutputFolders=$((totalOutputFolders+1))

  for file in "$dir"/*; do

    totalOutputFiles=$((totalOutputFiles+1))

  done
  
done

#all files and subfolders successfully copied or not
if [ $totalInputFolders -eq $totalOutputFolders ] &&  [ $totalInputFiles -eq $totalOutputFiles ]; then
  echo ""
  echo "All files and folders successfully compressed and copied."
else
  echo "Number of input and output files/dirs do not match"
fi

#calculate output filesize before and after compression script
OUTPUT_FOLDERSIZE_POST=$(du -sh $OUTPUT | cut -f1 | rev | cut -c 2- | rev)

#calculate compression ratio
COMPRESSION_RATIO=$(bc <<<"scale=2; $OUTPUT_FOLDERSIZE_POST / $OUTPUT_FOLDERSIZE_PRE")
COMPRESSION_RATIO="${COMPRESSION_RATIO:1}"

echo ""
echo "Script executed in $runtime seconds. Input folder - $INPUT - compressed to output folder - $OUTPUT - by ${COMPRESSION_RATIO}%, from ${OUTPUT_FOLDERSIZE_PRE}MB -> ${OUTPUT_FOLDERSIZE_POST}MB."
echo ""

