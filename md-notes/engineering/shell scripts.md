- export pikaichi reports for restaurant
```bash
#!/bin/bash

export TZ=Asia/Tokyo

reports=(
'ITEM'
'NIKKEI'
'NIKKEI_T'
'UCHIWAKE'
'NEWARI'
'KINKEN'
'KANSA'
)

export_pikaichi_ftp () {
target_dir=${1:-"''"}
business_date=$2 # format YYYY-MM-DD
workshift_id=${3:-"''"}
company_code=$4
merchant_code=$5
merchant_id=$6 # mmenu merchant id
ftp_host=${7:-"''"}
ftp_user=${8:-"''"}
ftp_password=${9:-"''"}

file_name_prefix="$(printf %05d $merchant_code)01$(date -d $business_date +%Y%m%d)$(date +%H%M%S)XXXX"
export_dir="/tmp/pikaichi_${merchant_id}_${business_date}"
mkdir -p $export_dir

for report in "${reports[@]}"; do
  if [[ "$workshift_id" == "''" ]]; then
    url="https://x.com/v2/third-party/pikaichi/export?lang=ja&merchantCode=$merchant_code&merchantId=$merchant_id&businessDate=$business_date&name=$report&fileNamePrefix=$file_name_prefix"
  else
    url="https://x.com/v2/third-party/pikaichi/export?lang=ja&merchantCode=$merchant_code&merchantId=$merchant_id&workshiftId=$workshift_id&businessDate=$business_date&name=$report&fileNamePrefix=$file_name_prefix"
  fi
  # echo $url
  curl -fsS $url > "$export_dir/${file_name_prefix}_${report}.csv"
done

zip_file="$file_name_prefix.zip"
cd $export_dir
zip -q -r $zip_file .

if [[ "$target_dir" != "''" ]]; then
  mv $zip_file $target_dir
fi

cd - &>/dev/null

if [[ "$ftp_host" != "''" ]]; then
lftp $ftp_host -u $ftp_user,$ftp_password <<END_SCRIPT
put "$export_dir/$zip_file"
quit
END_SCRIPT
fi

rm -rf $export_dir

sleep 1

}

# [business_date,to_date)
to_date=${to_date:-$(date -I -d "$business_date + 1 day")}
workshift_id=${workshift_id:-"''"}
target_dir=${target_dir:-"''"}

if [[ "$target_dir" != "''" ]]; then
  mkdir -p $target_dir
fi

while [ "$business_date" != $to_date ]; do
  echo $business_date
  # mac option for d decl (the +1d is equivalent to + 1 day)
  # business_date=$(date -j -v +1d -f "%Y-%m-%d" $business_date +%Y-%m-%d)
  jq -c '.[]' $pikaichi_restaurants_ftp_json | while read r; do
    export_pikaichi_ftp $target_dir $business_date $workshift_id $(echo $r | jq -r '[.companyCode,.merchantCode,.merchantId,.ftpHost,.ftpUser,.ftpPassword] | join(" ")')
  done
  business_date=$(date -I -d "$business_date + 1 day")
done

```