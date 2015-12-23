package preprocess;

import java.io.FileOutputStream;
import java.io.IOException;
 
import com.itextpdf.text.pdf.parser.ImageRenderInfo;
import com.itextpdf.text.pdf.parser.PdfImageObject;
import com.itextpdf.text.pdf.parser.RenderListener;
import com.itextpdf.text.pdf.parser.TextRenderInfo;
 
public class MyImageRenderListener implements RenderListener {
 
    /** The new document to which we've added a border rectangle. */
    protected String path = "";
 
    /**
     * Creates a RenderListener that will look for images.
     */
    public MyImageRenderListener(String path) {
        this.path = path;
    }
 
    public void renderImage(ImageRenderInfo renderInfo) {
        try {
            String filename;
            FileOutputStream os;
            PdfImageObject image = renderInfo.getImage();
            
            if (image == null) return;
            if (image.getImageAsBytes().length < 10000) {
            	return;
            }
            filename = String.format(path, renderInfo.getRef().getNumber(), image.getFileType());
            os = new FileOutputStream(filename);
            os.write(image.getImageAsBytes());
            os.flush();
            os.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

	@Override
	public void beginTextBlock() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void endTextBlock() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void renderText(TextRenderInfo arg0) {
		// TODO Auto-generated method stub
	}

}