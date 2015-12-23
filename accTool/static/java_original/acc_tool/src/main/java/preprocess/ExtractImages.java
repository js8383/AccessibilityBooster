package preprocess;

import java.io.IOException;

import com.itextpdf.text.DocumentException;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.parser.PdfReaderContentParser;

/**
 * Extracts images from a PDF file.
 */
public class ExtractImages {

	/** The new document to which we've added a border rectangle. */
//	public static final String RESULT = "src/main/input_pdf/output/Img%s.%s";
//	public static final String SRC = "src/main/input_pdf/input1.pdf";

	private String result;
	private String source;

	public ExtractImages(String source, String result) {
		this.source = source;
		this.result = result;
	}

	/**
	 * Parses a PDF and extracts all the images.
	 * 
	 * @param src
	 *            the source PDF
	 * @param dest
	 *            the resulting PDF
	 */
	public void extractImages() {
		PdfReader reader;
		
		try {
			
			reader = new PdfReader(source);

			PdfReaderContentParser parser = new PdfReaderContentParser(reader);
			MyImageRenderListener listener = new MyImageRenderListener(result);
			for (int i = 1; i <= reader.getNumberOfPages(); i++) {
				parser.processContent(i, listener);
			}
			reader.close();
		
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}