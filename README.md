# Project Summary: #

This project is a web application that stores and serves common coding interview
questions, concepts, and topics for anyone that needs interview practice. Users
on the website can also create their own content for others to view. This way
everyone can contribute and share the useful info on the website.

<br/>

# Installation: #  

### Step 1: Installing Required Files ###
___

**Required Programs and OS:**

  * **Windows 10**
  * **Python 3.6.5** - https://www.python.org/downloads/release/python-365/
  * **VirtualBox 5.1.38** - https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
  * **Vagrant 2.1.1** - https://www.vagrantup.com/downloads.html
  * **Git Bash 2.18.0** - https://git-scm.com/download/win

Must have the above programs before moving onto step 2!

<br/>

### Step 2: Readying Database Config ###
___


Once you have downloaded and installed the requirements, we can then download
the preloaded vagrant database configuration from my GitHub.

**Make sure to extract downloaded files to Desktop!**

<br/>

[Item-Catalog-App](https://github.com/mwz210/Item-Catalog-App)

<br/>

If all goes well, then you should see two additional folders on your desktop:

<br/>

  **1. Item-Catalog-App-master**  

<br/>


### Step 3: Finish Installation ###
___

If you have finished Step 1 and 2 then on your desktop you should have a folder
called Item-Catalog-App-master and within it, you should also see a folder called
vagrant.  


If the following files are in there then you are ready to run the project!

**1. catalog**
**2. Vagrantfile**

**Note: You may ignore the other files but don't delete them!**

<br/>

# Running the Project: #

### Getting into Linux System ###
___

First, open up Git Bash and then navigate to the folder **vagrant** within
the folder Item-Catalog-App-master on your Desktop.  

Once you have reached into the folder vagrant, I want you to run the following
commands while waiting in between each operation so they finish:

```
vagrant up
vagrant ssh
```  

**Note: the command 'vagrant up' will take a while since it is booting up your
linux OS in the virtual environment and command 'vagrant ssh' will allow you to
sign into the OS as a user which then means you can start using the Linux OS**  

<br/>

### Creating the database ###
___

You are almost there! Now that we are in the Linux OS on our shell session,
there is three more commands to run:  

```
cd ../../vagrant  
python database_setup.py
python fill_database.py  
```

Running these two commands will build the database this project works with.  

<br/>

### Run the Python File ###
___

Finally, we actually get to start the web application! Now within the Linux OS,
we should still be in the same location.

<br/>

Run the following command:

```
python project.py  
```

<br/>

If the above gives an error run this command instead:

```
python3 project.py
```

<br/>

Wait for a little and then go on your favorite web browser. In your browser,
visit http://localhost:8000 to see the wonder and not so wonderful project!.
