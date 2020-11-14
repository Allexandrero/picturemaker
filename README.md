# Picture Maker

This is a simple Flask picture converter, built into Docker-compose image.

## Usage

1. Download the package & extract it into preferred directory.
2. Move into extracted folder via terminal & run:
```
sudo docker-compose up web
```
> If you'd like to use Docker-compose as background process, you may add `-d` between `up` & `web`

3. There are 2 ways of how you can upload the picture:
  - With your web browser. Just proseed to `http://127.0.0.1:5000` or `localhost:5000`.
  
  - By Post-request from terminal. Just run this: 
  ```
  curl -F 'file=@YOUR_FILE_ADDRESS_HERE' -i "http://127.0.0.1:5000"
  ```

## Attention

If you use parser from web-form - you'll recieve a greyscale (512x512) version of image.

Also, if you use parser from terminal - you won't get the greyscale version of image, but, instead, information about the uploaded image in JSON format.

