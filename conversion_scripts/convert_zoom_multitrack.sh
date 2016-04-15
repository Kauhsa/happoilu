#!/usr/bin/env zsh

# is first parameter a folder?
input_directory="$1"
if [[ ! -d $input_directory ]]; then
  echo "heyo, first parameter should be a directory containing ZOOM****-folders"
  exit 1
fi

output_directory="$2"
if [[ ! -d $output_directory ]]; then
  echo "heyo, second parameter should be a directory where stuff is gonna be put"
  exit 1
fi

echo $merged_mp3_file_location
for current_directory in $(ls -d "$input_directory"/ZOOM*); do
  echo "###### Going to directory $current_directory, merging all .wav files for listening"

  input_files=("${(@f)$(ls $current_directory/*.WAV)}")
  ffmpeg_input_file_params=()
  for wav_file in $input_files; do
    ffmpeg_input_file_params+=("-i" "$wav_file")
  done

  merged_mp3_file_location="$(mktemp)"
  ffmpeg "${ffmpeg_input_file_params[@]}" -y -filter_complex amix=inputs="${#input_files}" -c:a libmp3lame -f mp3 -b:a 256k "$merged_mp3_file_location"
  echo "###### Done, launching file on mpv for listening (press Q when done)"
  mpv "$merged_mp3_file_location"

  vared -p '###### Give name for this file: ' -c file_prefix

  mkdir "$output_directory"/"$file_prefix"
  mv "$merged_mp3_file_location" "$output_directory"/"$file_prefix"/"$file_prefix"_merged.mp3
  for wav_file in $input_files; do
    wav_file_name="$output_directory"/"$file_prefix"/"$file_prefix"_$(basename "$wav_file" ".WAV").mp3
    ffmpeg -i "$wav_file" -c:a libmp3lame -f mp3 -b:a 256k "$wav_file_name"
  done
done