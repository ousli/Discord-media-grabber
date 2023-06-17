## Just a simple program to download all your Discord media
1. Download your data from the Discord app by going to **Settings > Privacy and Security > Request all my data**.
2. Unzip the downloaded file once you receive it.
3. Install the **requests** library by running ``pip install requests``.
4. Copy the absolute path of the "messages" folder located inside your Discord backup.
5. Run the ``main.py`` file.
6. Paste the copied absolute path when prompted.
7. The program will now proceed to download all your media files into a new folder named **result**, which will be created inside the "messages" folder.