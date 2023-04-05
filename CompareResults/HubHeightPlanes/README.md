# Hub height plane comparisons

The following document describes the file format and process for creating the hub-height planes for comparison.

## Writing out the pickle file
So as long as you can get your hub-height plane loaded into python and you can do this 
```python
   c=ax.contourf(xm, ym, np.sqrt(vx**2 + vy**2), cmap='coolwarm')
```
We can use it for our comparison.  

To write out the pickle file, then all you should need to do is something like this:
```python
        # Create a fresh db dictionary
        db = {}
        db['x'] = xm
        db['y'] = ym
        db['z'] = zm        
        db['vx'] = vx
        db['vy'] = vy
        db['vz'] = vz

        # Write out the picklefile
        dbfile = open(pklfilename, 'wb')
        pickle.dump(db, dbfile, protocol=2)   # Note to use protocol=2 for maximum compatibility
        dbfile.close()
```

An example of a script that we use to create the hub-height planes from AMR-Wind netcdf data is [here](https://github.com/lawrenceccheung/AWAKEN_summit_setup/blob/main/CompareResults/HubHeightPlanes/Unstable/DATA_Summit_amrwind_bananasrun1/makeInstPkl.py).

## Fields to output
If possible, from both the precursor run and the turbine run simulations, output the Vx, Vy, and Vz components for the 
1.	Instantaneous velocity field
2.	Mean velocity field
3.	Standard deviation of the velocity field
That would nominally be 6 pickle files for each case.  For FLORIS runs, #1 and #2 could end up being the same thing, and the precursor field could be just a constant so no need to do that.  If you’re tight on time, I would prioritize things in exactly this order: do the instantaneous first, then means, and then standard deviations.

## Where to store the pickle files
If your pickle files are small (less than a few megabytes), you can store these binary files directly in the github repo.  However, because these velocity field files could get big (hundreds of MB’s), we don’t want to exceed the github quota just storing these pickle files.  So what we’re going to do is to store the link to the data file themselves, instead of the entire file.

In theory, you can place your files in any publicly accessible file sharing system, like dropbox or google drive, but we can hijack one functionality of github to do the file storage for us.  The github releases page allow you store binaries without any quota limit (as long as each individual file is under 2Gb).

Once you’re generated those pickle files, upload them to the release page at https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/tag/v0.0.0-temp1. (Just click on the pencil button to “edit release” and drag/drop your files into the Assets section).   Be sure to use a unique file name convention for your pickle files, as everybody is going to call it “KingPlains_mean.pkl” otherwise.

## Editing the YAML file
Once you have the pickle files committed or uploaded somewhere, we just need to create a yaml file which describes the data files and their location.  An example of it would be at [DATA_Summit_unstable.yaml](https://github.com/lawrenceccheung/AWAKEN_summit_setup/blob/main/CompareResults/HubHeightPlanes/Unstable/DATA_Summit_amrwind_bananasrun1/DATA_Summit_unstable.yaml), and you can see the basic form of it below: 

```yaml
KingPlains:
  instantaneous:
    turbinerun:
      filename: DATA_Summit_unstable_bananas1_KP_z90_wturb_inst_900.pkl
      url: https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/download/v0.0.0-temp1/DATA_Summit_unstable_bananas1_KP_z90_wturb_inst_900.pkl
    precursorrun:
      filename: DATA_Summit_unstable_bananas1_KP_z90_noturb_inst_900.pkl
      url: https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/download/v0.0.0-temp1/DATA_Summit_unstable_bananas1_KP_z90_noturb_inst_900.pkl
  mean:
    turbinerun:
      filename: DATA_Summit_unstable_bananas1_KP_z90_wturb_mean_900.pkl
      url: https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/download/v0.0.0-temp1/DATA_Summit_unstable_bananas1_KP_z90_wturb_mean_900.pkl
    precursorrun:
      filename: DATA_Summit_unstable_bananas1_KP_z90_noturb_mean_900.pkl
      url: https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/download/v0.0.0-temp1/DATA_Summit_unstable_bananas1_KP_z90_noturb_mean_900.pkl
  std:
    turbinerun:
      filename: DATA_Summit_unstable_bananas1_KP_z90_wturb_std_900.pkl
      url: https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/download/v0.0.0-temp1/DATA_Summit_unstable_bananas1_KP_z90_wturb_std_900.pkl
    precursorrun:
      filename: DATA_Summit_unstable_bananas1_KP_z90_noturb_std_900.pkl
      url: https://github.com/lawrenceccheung/AWAKEN_summit_setup/releases/download/v0.0.0-temp1/DATA_Summit_unstable_bananas1_KP_z90_noturb_std_900.pkl
```
If your pickle files were sufficiently small to be committed to the repo itself, then the `url` field can be left blank.
