# Taskite

Open source Trello, JIRA, Asana alternative.

# Installation

Create a file called .env in the root folder and paste all the contents of .env.dist into it.

## Requirements
1. PostgreSQL Database
2. Minio Server (For object storage)
3. Python3 installed
4. Nodejs installed

## 1. Setting up PostgreSQL server
If you don't have postgresql installed on your system, then you can refer the [docs](https://www.postgresql.org/download/) for installing the same.



## 2. Setting up minio server
For installing minioserver please refer the for installing as per the operating system.
[MacOS](https://min.io/docs/minio/macos/index.html)
[Linux](https://min.io/docs/minio/linux/index.html)

For starting the minioserver use the following command
```
minio server $(pwd)/media/minio --console-address :9001
```

Then visit [localhost:9001](http://localhost:9001) to open minio admin panel.
Default username and password are minioserver and minioserver respectively.

1. Go to [policies](http://127.0.0.1:9001/policies)
2. Click on Create Policy
3. Enter policy name as takite and in the write policy section copy paste the following code.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::taskite",
                "arn:aws:s3:::taskite/uploads/*"
            ]
        }
    ]
}
```
4. Go to [users](http://127.0.0.1:9001/identity/users) under Identity section.
5. Click on Create User.
6. Give User Name as taskite and password as password.
7. In Select Policy section select taskite policy.
8. Go to [users]((http://127.0.0.1:9001/identity/users)) under Identity and select taskite.
9. Select Service Accounts and click on Create Access Key
10. Copy the Access Key and paste it under AWS_ACCESS_KEY in .env file
11. Copy the Secret Key and past it under AWS_SECRET_KEY in .env file
12. Click on Create and download the .csv file in case of keys goes missing.

Yaah! Your blob storage is ready to be used as a media store for the project.

## 3. Setting up python server
Make sure python3 is installed on your system
1. We need to setup a virtual environment so that we install our project dependecies inside that. Run the following command to initate a virtual environment
```
python3 -m venv .venv
```
2. After this you could see a folder called .venv has been created, now let's activate it. Based on different operating system the activation command can vary.

MacOS/Linux
```
source .venv/bin/activate
```

Windows
```
source .venv\Scripts\activate.bat
```

3. Now let's install the dependencies
```
python3 install -r requirements-dev.txt
```

Once done, our django server is ready to be server. Run the below command to start the backend server
```
python3 manage.py runserver
```

## 4. Setting up frontend server
First we need to install the node dependencies.
Run the below command to install all the node packages
```
npm install
```

To start the frontend server
```
npm run dev
```


