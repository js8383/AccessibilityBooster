package preprocess;

import java.awt.image.BufferedImage;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;

import com.itextpdf.text.*;
import com.itextpdf.text.pdf.PRStream;
import com.itextpdf.text.pdf.PdfArray;
import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfImage;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.PdfStamper;
import com.itextpdf.text.pdf.PdfStream;
import com.itextpdf.text.pdf.PdfString;
import com.itextpdf.text.pdf.parser.PdfImageObject;

public class ImagetagParser {

	private String result;
	private String source;

	public ImagetagParser(String source, String result) {
		this.source = source;
		this.result = result;
	}

	public void outputTags() {

		try {

			PdfReader reader = new PdfReader(source);
			PdfDictionary catalog = reader.getCatalog();
			PdfDictionary structTreeRoot = catalog
					.getAsDict(PdfName.STRUCTTREEROOT);

			//
			List<PdfDictionary> figureDictsList = extractFiguureDict(structTreeRoot);
			//

			File fout = new File(result);
			FileOutputStream fos;

			fos = new FileOutputStream(fout);

			BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));

			for (PdfDictionary pd : figureDictsList) {
				// System.out.println(1);
				if (pd.get(PdfName.ALT) == null) {
					bw.write("None");
				} else {
					bw.write(pd.get(PdfName.ALT).toString());
				}
				bw.newLine();
			}
			bw.close();

		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	public List<PdfDictionary> extractFiguureDict(PdfDictionary element) {

		List<PdfDictionary> figureDictsList = new ArrayList<PdfDictionary>();

		if (element == null) {
			// System.out.println("Null structure tree root!");
			return figureDictsList;
		}

		if (PdfName.FIGURE.equals(element.get(PdfName.S))) {
			figureDictsList.add(element);
		}

		PdfDictionary dictKids = element.getAsDict(PdfName.K);
		if (dictKids != null) {
			figureDictsList.addAll(extractFiguureDict(dictKids));
		}

		PdfArray arrayKids = element.getAsArray(PdfName.K);
		if (arrayKids == null) {
			// System.out.println("Null kids");
			return figureDictsList;
		}
		for (int i = 0; i < arrayKids.size(); i++) {
			figureDictsList.addAll(extractFiguureDict(arrayKids.getAsDict(i)));
		}

		return figureDictsList;
	}
}
