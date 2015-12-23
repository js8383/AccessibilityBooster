package output;

import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
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

public class AddAlttext {

	private String result;
	private String source;
	private String ref;
	
	public AddAlttext(String source, String result, String ref) {
		this.source = source;
		this.result = result;
		this.ref = ref;
	}

	public void outputPdf() {
		List<String> tags = new ArrayList<String>();

		try {

			PdfReader reader = new PdfReader(source);
			PdfDictionary catalog = reader.getCatalog();
			PdfDictionary structTreeRoot = catalog
					.getAsDict(PdfName.STRUCTTREEROOT);

			//
			List<PdfDictionary> figureDictsList = extractFiguureDict(structTreeRoot);
			//

			File fin = new File(ref);

			BufferedReader br = new BufferedReader(new FileReader(fin));

			String line = null;
			while ((line = br.readLine()) != null) {
//				System.out.println(line);
				tags.add(line);
			}

			br.close();

			int i = 0;
			int s = tags.size();
			for (PdfDictionary pd : figureDictsList) {
				if (i < s && !tags.get(i).equals("None")) {
					pd.put(PdfName.ALT, new PdfString(tags.get(i)));
				}
				i++;
			}

			PdfStamper stamper = new PdfStamper(reader, new FileOutputStream(
					result));
			stamper.close();

		} catch (IOException | DocumentException e) {
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
