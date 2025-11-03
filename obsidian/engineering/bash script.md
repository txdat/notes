# pikaichi ftp
```bash
#!/bin/bash

# pikaichi_restaurants_ftp.json
# [
#   {
#     "companyCode": 100,
#     "merchantCode": 1000,
#     "merchantId": "",
#     "ftpHost": "",
#     "ftpUser": "",
#     "ftpPassword": "",
#     "from": "",
#     "to": "",
#     "dates": "", // dates are separated by comma
#   },
#   ...
# ]

export TZ=Asia/Tokyo

reports=(
'ITEM'
'NIKKEI'
'NIKKEI_T'
'UCHIWAKE'
'NEWARI'
'KINKEN'
'KANSA'
'FREE'
)

export_pikaichi_ftp () {
target_dir=${1:-"''"}
business_date=$2 # format YYYY-MM-DD
workshift_id=${3:-"''"}
company_code=$4
merchant_code=$5
merchant_id=$6 # mmenu merchant id
pos_id_code=${7:-"XXXX"}
ftp_host=${8:-"''"}
ftp_user=${9:-"''"}
ftp_password=${10:-"''"}
ftp_mode=${11:-"''"}
use_business_date_in_report=${12:-"true"}

file_name_prefix="$(printf %05d $merchant_code)01$(date -d $business_date +%Y%m%d)$(date +%H%M%S)${pos_id_code}"
export_dir="/tmp/pikaichi_${merchant_id}_${business_date}"
mkdir -p $export_dir

base_url="http://localhost:3000/pikaichi/export"

for report in "${reports[@]}"; do
  if [[ "$workshift_id" == "''" ]]; then
    url="$base_url?lang=ja&merchantCode=$merchant_code&merchantId=$merchant_id&businessDate=$business_date&name=$report&fileNamePrefix=$file_name_prefix&useBusinessDateInReport=$use_business_date_in_report"
  else
    url="$base_url?lang=ja&merchantCode=$merchant_code&merchantId=$merchant_id&businessDate=$business_date&name=$report&fileNamePrefix=$file_name_prefix&workshiftId=$workshift_id&useBusinessDateInReport=$use_business_date_in_report"
  fi
  # echo $url
  file="$export_dir/${file_name_prefix}_${report}.csv"
  curl -fsS $url > $file
  echo $file $(cat $file | wc -l)
done

zip_file="$file_name_prefix.zip"
cd $export_dir
zip -q -r $zip_file .

if [[ "$target_dir" != "''" ]]; then
  cp $zip_file $target_dir
fi

cd - &>/dev/null

ftp_log_file="$export_dir/ftp.log"
if [[ "$ftp_host" != "''" ]]; then
  if [[ "$ftp_mode" == "pasv" ]]; then
    echo "Sending files in passive mode"
    lftp $ftp_host -u $ftp_user,$ftp_password -e "set ftp:ssl-allow no; set ftp:passive-mode on; set xfer:log 1; debug 3; put "$export_dir/$zip_file"; exit" > $ftp_log_file 2>&1
  else
    lftp $ftp_host -u $ftp_user,$ftp_password -e "set xfer:log 1; debug 3; put "$export_dir/$zip_file"; exit" > $ftp_log_file 2>&1
  fi
fi

# Check the exit status of lftp
if [ $? -ne 0 ]; then
  echo "File upload failed." $(du -sh "$export_dir/$zip_file")
  rm -rf $export_dir
  return 1
elif [ -f "$ftp_log_file" ] && grep -iE "failed|error|denied|cannot|timeout" $ftp_log_file; then
  echo "File upload failed." $(du -sh "$export_dir/$zip_file")
  rm -rf $export_dir
  return 1
else
  echo "File uploaded successfully." $(du -sh "$export_dir/$zip_file")
  rm -rf $export_dir
  return 0
fi
}

# [from_date,to_date)
to_date=${to_date:-$(date -I -d "$from_date + 1 day")}
workshift_id=${workshift_id:-"''"}
target_dir=${target_dir:-"''"}

if [[ "$target_dir" != "''" ]]; then
  mkdir -p $target_dir
fi

jq -c '.[]' $pikaichi_restaurants_ftp_json | while read r; do
  from_date=$(echo $r | jq -r '.from')
  to_date_r=$(echo $r | jq -r '.to')
  dates=$(echo $r | jq -r '.dates')

  if [[ -n "$from_date" && -n "$to_date_r" && "$from_date" != "null" && "$to_date_r" != "null" ]]; then
    current_date=$from_date
    while [ "$current_date" != "$to_date_r" ]; do
      echo $current_date
      export_pikaichi_ftp $target_dir $current_date $workshift_id $(echo $r | jq -r '[.companyCode,.merchantCode,.merchantId,.posIdCode,.ftpHost,.ftpUser,.ftpPassword,.ftpMode] | join(" ")')
      current_date=$(date -I -d "$current_date + 1 day")
    done
  elif [[ -n "$dates" && "$dates" != "null" ]]; then
    IFS=',' read -ra date_array <<< "$dates"
    for date in "${date_array[@]}"; do
      echo $date
      export_pikaichi_ftp $target_dir $date $workshift_id $(echo $r | jq -r '[.companyCode,.merchantCode,.merchantId,.posIdCode,.ftpHost,.ftpUser,.ftpPassword,.ftpMode] | join(" ")')
    done
  else
    current_date=$from_date
    while [ "$current_date" != "$to_date" ]; do
      echo $current_date
      export_pikaichi_ftp $target_dir $current_date $workshift_id $(echo $r | jq -r '[.companyCode,.merchantCode,.merchantId,.posIdCode,.ftpHost,.ftpUser,.ftpPassword,.ftpMode] | join(" ")')
      current_date=$(date -I -d "$current_date + 1 day")
    done
  fi
done

```