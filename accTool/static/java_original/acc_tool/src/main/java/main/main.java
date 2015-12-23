package main;

import output.AddAlttext;
import preprocess.ExtractImages;
import preprocess.ImagetagParser;

public class main {

	public static void main(String[] args) {
		String option = args[0];
		if (option.equals("-p")) {
			String inputFile = args[1];
			String outputImage = args[2];
			String outputAltText = args[3];

			ExtractImages extractImages = new ExtractImages(inputFile,
					outputImage);
			extractImages.extractImages();
			ImagetagParser imagetagParser = new ImagetagParser(inputFile,
					outputAltText);
			imagetagParser.outputTags();
		}
		
		if (option.equals("-o")) {
			String inputFile = args[1];
			String outputPdf = args[2];
			String intputTextFile = args[3];

			AddAlttext addAlttext = new AddAlttext(inputFile, outputPdf, intputTextFile);
			addAlttext.outputPdf();
		}
	}

}
