# temperature-in-my-house

내방의 온도를 측정하여 database 에 넣기 위한 프로젝트

1. __raspberry 4B__ 에서 DHT22 센서를 이용해 온습도 데이터를 수집합니다.  ([cj-rasp](https://github.com/noname2048/cj-rasp))
2. 수집된 데이터를 requests 를 통해 aws-lambda 로 전달합니다.
3. aws-lambda 는 supabase postgresql 데이터 베이스에 넣습니다.

기타사항
- raspberry pi는 재부팅시에도 온도를 자동으로 수집할 수 있도록, systemctl 혹은 crontab 을 이용합니다.
- aws-lambda 는 필요한 파이썬 패키지를 포장하여 layer로 등록합니다.

## make lambda layer

해당 블로그를 참조하여 진행하였습니다.
- https://www.linkedin.com/pulse/add-external-python-libraries-aws-lambda-using-layers-gabe-olokun/

1. `cd aws-lambda/packages`
2. poetry 등을 이용해 패키지를 다운로드 합니다. `poetry add supabase`
3. requirements.txt 에 필요한 패키지를 기록합니다. `pip frezze > requirements.txt`
4. 해당패키지들을 python 폴더에 설치합니다. `pip3 install -r requirements -t python`
5. 해당 python 폴더를 zip 합니다. `zip -r lamb_pack python`
6. 해당 zip 폴더를 업로드 합니다. aws를 사용하 수도 있습니다. `aws s3 cp python s3://<your-bucket-name>`
