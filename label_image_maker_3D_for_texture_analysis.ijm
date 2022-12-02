
close("*");

dirData = getDirectory("Choose a Directory Corrected files");
listData = getFileList(dirData);
n1 = lengthOf(listData);
print(n1);

dirMask = getDirectory("Choose a Directory masks");
listMask = getFileList(dirMask);
n2 = lengthOf(listMask);
print(n2);

dirSave = getDirectory("Choose a Directory SAVE");

//---------------------------------

close("*");

//---------------------------------

//Open and display images
	
	//setBatchMode(true);
	//setBatchMode("show");
    for (i=0; i<n1; i++) {

	pathData = dirData+listData[i];
	open(pathData);

	//split channels and close C2
	selectedFile = getTitle();
	rename("original");
	run("Split Channels");
	channel1 = "C1-"+"original";
	channel2 = "C2-"+"original";
	selectImage(channel2);	
	close;
	
	//make max projection of ch2
	selectImage(channel1);
	run("Z Project...", "projection=[Max Intensity]");
	rename("ch1");
	
	selectImage(channel1);		//close old image
	close;
	
	selectWindow("ch1");
	run("Enhance Contrast", "saturated=0.35");
	run("8-bit");
	
	//open mask
	pathMask = dirMask+listMask[i];
	open(pathMask);
	rename("mask");
	run("Z Project...", "projection=[Max Intensity]");
	selectWindow("mask");
	close;
	selectWindow("MAX_mask");
	run("Options...", "iterations=6 count=1 black");
	run("Dilate");
	run("Fill Holes");
	
//Create Labels

	// select mask to be edited
	selectWindow("MAX_mask");
	
	//set drawing options
	run("Colors...", "foreground=black background=black selection=pink");
	run("Line Width...", "line=4");
	setTool("freeline");
	waitForUser("Please correct segmentation by 1.Draw a line 2) Press letter d. If you want to delete something, select freehand selection tool from the toolbar, draw around area to be deleted and click backspace. Then click OK");
	run("Select None");
	
	//create labels
	run("Analyze Particles...", "size=5000-Infinity show=[Count Masks]");
	run("8-bit");
	saveAs("Tiff", dirSave + selectedFile + "_mask");


	close("*");

	}


