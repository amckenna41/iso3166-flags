#!/bin/bash

############################## SVG Compress ##############################

# SVG files can be quite large in size but a lot of its data can be
# redundant or unnecessary information so I created this script to help
# maximise the storage of the files, especially since the output folder may
# contain thousands of files. The script utilises the scour Python library
# to compress the output SVG files if they meet a specific threshold of
# file size. These files are then copied to the output folder. If file size
# threshold is not met or the file is not an SVG then the original file is
# copied to the output. Any other image file types such as png, jpg or gif
# are copied to the output folder.
#
# Works on both the flat iso3166-1-flags layout and the nested
# iso3166-2-flags/<country>/ layout - the input's sub-folder structure
# is mirrored in the output folder.

##########################################################################

#Help Funtion showing script usage
Help()
{
   echo "Bash Script for compressing SVG files if they are above certain file size threshold."
   echo ""
   echo "Basic Usage, using default parameters: ./svg_compress.sh "
   echo "Usage: ./svg_compress.sh [--input --output --filesize]"
   echo ""
   echo "Options:"
   echo "-h          help"
   echo "-input      Path to input directory of flags to compress (flat or nested by country)."
   echo "-output     Path to output directory to store compressed SVG files."
   echo "-filesize   File size threshold in KB, if file above it then execute compression algorithm."
   exit
}

#parse all input arguments
for i in "$@"
do
case $i in
    -i=*|--input=*)
    INPUT="${i#*=}"
    ;;
    -o=*|--output=*)
    OUTPUT="${i#*=}"
    ;;
    -f=*|--filesize=*)
    FILESIZE_THRESHOLD="${i#*=}"
    ;;
    -h|--h|--help)
    Help
    ;;
    *)
    echo "Unknown option: $i" && exit 1
    ;;
esac
done

#set default values for input parameters if empty, strip any trailing slash
INPUT="${INPUT:-countries}"; INPUT="${INPUT%/}"
OUTPUT="${OUTPUT:-outputs}"; OUTPUT="${OUTPUT%/}"
FILESIZE_THRESHOLD="${FILESIZE_THRESHOLD:-50}"

#check input dir exists and scour is available, create output dir
[ ! -d "$INPUT" ] && echo "Input directory path does not exist." && exit 1
#use the scour CLI if it runs, otherwise fall back to the Python module (e.g. a stale/wrong-arch CLI on the PATH)
SCOUR=(scour)
"${SCOUR[@]}" --version >/dev/null 2>&1 || SCOUR=(python3 -m scour.scour)
"${SCOUR[@]}" --version >/dev/null 2>&1 || { echo "scour not found, install with: pip install scour"; exit 1; }
mkdir -p "$OUTPUT"

#input folder size in KB, before compression
INPUT_SIZE_KB=$(du -sk "$INPUT" | cut -f1)

#start time of script
start=$(date +%s)

echo ""
echo "##############################################"
echo "Compressing SVG Files using scour algorithm..."
echo ""
echo "Input Folder: $INPUT"
echo "Output Folder: $OUTPUT"
echo "File Size Threshold: $FILESIZE_THRESHOLD KB"
echo ""
echo "#############################################"
echo ""

totalInputFiles=0

#iterate through every file in the input dir (any depth), compressing SVGs over the KB threshold and copying everything to the output dir
while IFS= read -r -d '' file; do

  #skip README/DS_Store files
  bname="$(basename -- "$file")"
  [[ "$bname" == "README.md" || "$bname" == ".DS_Store" ]] && continue
  totalInputFiles=$((totalInputFiles+1))

  #mirror the file's sub-folder (if any) in the output dir
  relPath="${file#"$INPUT"/}"
  outputPath="$OUTPUT/$relPath"
  mkdir -p "$(dirname -- "$outputPath")"
  extension="${bname##*.}"

  #if output file already exists then skip to next file
  if [ -f "$outputPath" ]; then
    echo "Output File $outputPath already exists."
    continue
  fi

  #if input file is gif, convert to png (requires ImageMagick)
  if [[ "$extension" == "gif" ]] && command -v convert >/dev/null 2>&1; then
    convert "$file" "${outputPath%.*}.png"
    continue
  fi

  #if file type != .svg (is png or jpg) then continue but still copy file to outputs
  if [[ "$extension" != "svg" ]]; then
    cp "$file" "$outputPath"
    continue
  fi

  #get file size in KB
  filesize=$(( $(wc -c < "$file") / 1024 ))

  #if file size > threshold, compress SVG using scour library
  if (( filesize > FILESIZE_THRESHOLD )); then
    echo "Compressing $relPath (${filesize}KB)"
    "${SCOUR[@]}" -i "$file" -o "$outputPath" --enable-viewboxing --enable-id-stripping \
      --enable-comment-stripping --shorten-ids --indent=none -q
  else
    #copy files less than threshold to outputs folder
    cp "$file" "$outputPath"
  fi

done < <(find "$INPUT" -type f -not -path "$OUTPUT/*" -print0)

#end time of script, calculate total runtime
end=$(date +%s)
runtime=$((end-start))

#validate the same number of files are in the INPUT and OUTPUT folders, ensuring all files are compressed and/or copied over
totalOutputFiles=$(find "$OUTPUT" -type f -not -name README.md -not -name .DS_Store | wc -l | tr -d ' ')
echo ""
if [ "$totalInputFiles" -eq "$totalOutputFiles" ]; then
  echo "All $totalInputFiles files successfully compressed and copied."
else
  echo "Number of input ($totalInputFiles) and output ($totalOutputFiles) files do not match."
fi

#calculate the size reduction - du -sk gives both sizes in KB so they're directly comparable
OUTPUT_SIZE_KB=$(du -sk "$OUTPUT" | cut -f1)
REDUCTION=$(awk -v pre="$INPUT_SIZE_KB" -v post="$OUTPUT_SIZE_KB" 'BEGIN { printf "%.1f", pre ? (pre - post) * 100 / pre : 0 }')

echo ""
echo "Script executed in $runtime seconds. Input folder - $INPUT - compressed to output folder - $OUTPUT - reduced by ${REDUCTION}%, from ${INPUT_SIZE_KB}KB -> ${OUTPUT_SIZE_KB}KB."
