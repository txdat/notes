- export pikaichi reports for restaurant
```bash
#!/bin/bash

# pikaichi_restaurants_ftp.json
# [
#   {
#     "companyCode": 100,
#     "merchantCode": 1001,
#     "merchantId": "6536381804e556a260dcd4b4",
#     "ftpHost": "",
#     "ftpUser": "",
#     "ftpPassword": ""
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
)

export_pikaichi_ftp () {
business_date=$1
workshift_id=$2
company_code=$3
merchant_code=$4
merchant_id=$5
ftp_host=$6
ftp_user=$7
ftp_password=$8

file_name_prefix="$(printf %05d $merchant_code)01$(date -d $business_date +%Y%m%d)$(date +%H%M%S)XXXX"
export_dir="/tmp/pikaichi/${merchant_id}_${business_date}"
mkdir -p $export_dir

for report in "${reports[@]}"; do
  url="https://api.mmenu.io/v2/third-party/pikaichi/export?lang=ja&merchantCode=$merchant_code&merchantId=$merchant_id&workshiftId=$workshift_id&businessDate=$business_date&name=$report&fileNamePrefix=$file_name_prefix"
  curl -s $url > "$export_dir/${file_name_prefix}_${report}.csv"
done

zip_file="$file_name_prefix.zip"
cd $export_dir
zip -q -r $zip_file .
cd - &>/dev/null

# lftp $ftp_host -u $ftp_user,$ftp_password <<END_SCRIPT
# put "$export_dir/$zip_file"
# quit
# END_SCRIPT
#
# rm -rf $export_dir
}

jq -c '.[]' $pikaichi_restaurants_ftp_json | while read merchant; do
  merchant_config=$(echo $merchant | jq -r '[.companyCode,.merchantCode,.merchantId,.ftpHost,.ftpUser,.ftpPassword] | join(" ")')
  echo $r | jq -c '.workshifts.[]' | while read workshift; do
    workshift_config=$(echo $workshift | jq -r '[.businessDate,.workshiftId] | join(" ")')
    export_pikaichi_ftp $workshift_config $merchant_config
  done
done
```