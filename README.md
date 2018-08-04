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

[FSND-Virtual-Machine](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)

[newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

<br/>

If all goes well, then you should see two additional folders on your desktop:

<br/>

  **1. newsdata-1**  

  **2. FSND-Virtual-Machine**

<br/>

Now, move the file **newsdata.sql** within newsdata folder into the folder
**vagrant** within FSND-Virtual-Machine.  

<br/>

To actually run this project, we will need to have **logs.py**, which is in this
GitHub repository, to be inside folder vagrant as well. Download logs.py and
move it into vagrant.

<br/>

### Step 3: Finish Installation ###
___

If you have finished Step 1 and 2 then on your desktop you should have a folder
called FSND-Virtual-Machine and within it, you should also see a file called
vagrant.  

Go into the vagrant folder and check if you have the files **newsdata.sql** and
**logs.py**.

If both files are in there then you are ready to run the project!

<br/>

# Running the Project: #

### Getting into Linux System ###
___

First, open up Git Bash and then navigate to the folder **vagrant** within
the folder FSND-Virtual-Machine on your Desktop.  

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
there is two more commands to run:  

```
cd ../../vagrant  
psql -d news -f newsdata.sql  
```

Running these two commands will build the database this project works with.  

<br/>

### Run the Python File ###
___

Finally, we actually get to see our reports! Now within the Linux OS, we should
still be in the same location.

<br/>

Run the following command:

```
python logs.py  
```

<br/>

If the above gives an error run this command instead:

```
python3 logs.py
```

<br/>

Wait for a little and the reports will come in! A sample report is in the
example_output.txt and its provided within this same repository.
