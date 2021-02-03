#!/bin/bash

export https_proxy="socks5://127.0.0.1:2345"

baseurl=`yq r .archivessnake.yml baseurl`
username=`yq r .archivessnake.yml username`
password=`yq r .archivessnake.yml password`


SESSION=`curl -s -F password=$password $baseurl/users/$username/login | jq -r '.session'`


test_fn () {
  # echo "testing $1"
  curl -H "X-ArchivesSpace-Session: $SESSION" \
  $baseurl/repositories/2/archival_objects/${1}

}

delete_ao () {
  curl -H "X-ArchivesSpace-Session: $SESSION" \
  -X DELETE $baseurl/repositories/2/archival_objects/${1}

}


ids=(
    # 559048
    # 554622
    # 554631
    # 554655
    # 556882
    # 556989
    # 554667
    # 554687
    # 554692
    # 555996
    # 559246
    # 554727
    # 554731
    # 555968
    # 558069
    # 554753
    # 556093
    # 554769
    # 554813
    # 557808
    # 554820
    554830
    554835
    556260
    559859
    554931
    559906
    554396
    559766
    558426
    560574
    558914
    555106
    555112
    555114
    554512
    557116
    555263
    558376
    557786
    560297
    555283
    555284
    555286
    560422
    555289
    555290
    560337
    555297
    555298
    555300
    555302
    555303
    555306
    560421
    560152
    557250
    555314
    557328
    557332
    555315
    557794
    554519
    555322
    557092
    555326
    555328
    554552
    555329
    560142
    555338
    )

for i in "${ids[@]}"
do
    echo "looking up $i"
    test_fn $i
    echo "deleting $i"
    delete_ao $i
done

# test_fn "30"

exit







