# Run a group behavioural study

This page gives a check-list of what to do to run a group study in the Design 2 room (0.83.14).

## Checklist: 

1. Book the room

2. Install your experiment in the room, and test

3. Create an evento link 

4. Prepare consent forms and gift vouchers

5. Advertise the experiment

6. Run experiment


## Booking the room

- First check the availability of the room on the ENSMM calendar: [https://edt.ens2m.fr/2022-2023/invite](https://edt.ens2m.fr/2022-2023/invite), navigate to "Salles" (rooms), type room number ("0.83.14 (Transfert-Salle Design 2)")

- Then send an email to the ENSMM admin staff so that they book the room for you at your specific timeslots (perhaps give yourself 30min ahead and before for security). Our contact for this is Mrs Charlotte VITALI (charlotte.vitali@ens2m.fr). Mention something along these lines:

> _Bonjour Mme Vitali,_ \
> \
> _Je suis XXX et je travaille dans le Département AS2M du laboratoire FEMTO-ST, dans l'équipe de Jean-Julien Aucouturier._ \
> \
> _Nous aurions besoin d'utiliser la salle Design 2 (0.83.14) du bâtiment Transfert pour une expérience pour nos travaux de recherche, et nous aimerions réserver les créneaux suivants:_ \
> \
> _- day/month, from hour to hour_\
> _- day/month, from hour to hour_\
> \
> \
> _Merci beaucoup !_\
> _XXX_


## Installing the experiment + testing it

### Installation 

These instructions are for experiments running with Python / psychopy. The main difficulty is that computers in room Design 2 are administered centrally by the SUPMICROTECH IT services and, while they run python, we cannot install external libs like psychopy permanently: 

- first, because in order to participate, your participants will need to log in each machine with their personal `ens2m.fr` id, and we therefore cannot install python libraries to every account (which we do not have access to in advance). 

- second, because even if we did, all computer installations are wiped and reinstalled every night, so we'd have to reinstall next time anyway. 

To solve this problem, we need to copy all needed libraries locally: 

Assuming your experiment directory structure is something like the following:

    ```
    my_experiment
    |-- experiment
	    |-- experiment.py
	    |-- data
    |-- libs
    ```

1. Log in to the machine with your ens2m.fr id (see [this page](../becoming-a-lab-member/lab-registration-procedure/) for getting an ENSMM account if you don't have one)

2. Copy the `my_experiment` folder into `Partage Enseignements/Neuro/`

3.  Run:

    ```sh
    cd path/to/my_experiment
    pip install -t ./libs/ psychopy
    ```
to install all needed libraries to the `/libs` folder (do the same for every library needed for your code to run) 

    !!! Warning
        This cannot be prepared in advance on your own computer, because you should run the `pip` command corresponding to the version of `python` that's installed on the ensmm computers. 

    !!! Note
        `pip install psychopy` tends to install a lot of unnecessary librairies, you may want to `pip install -t ./libs/ --no-deps psychopy` instead, and reiterate with all needed libraries until your code works ==check syntax== 

1.  At the top of the experiment script, add the following lines so that your code loads libraries from the `\libs` folder:

    ```python
    import sys
    sys.path.append(../libs) 
    ```

1.  In `my_experiment/experiment/` create a `run.bat` file with the following:

    ```
    @echo off
    python ./experiment.py %*
    ```

### Testing 

The procedure for every participant is to 

1. Log in with ens2m.fr id

2. Copy `my_experiment` folder from `Partage Enseignements/Neuro` to `Desktop/` (takes a few minutes)

3. Run `run.bat`


