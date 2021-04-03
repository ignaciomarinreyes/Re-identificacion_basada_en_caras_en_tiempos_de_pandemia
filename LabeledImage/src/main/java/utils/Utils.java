package utils;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class Utils {

    private FileWriter fichero;
    private PrintWriter pw;
    private String path;

    public Utils(String nameFile, String path) {
        this.path = path;
        int pos = nameFile.lastIndexOf(".");  
        try {
            this.fichero = new FileWriter(this.path + "/" + nameFile.substring(0,pos) + "_tagged.txt");
            this.pw = new PrintWriter(fichero);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    public void changeFile(String nameFile) {
        int pos = nameFile.lastIndexOf(".");  
        try {
            if (null != fichero) {
                fichero.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            this.fichero = new FileWriter(this.path + "/" + nameFile.substring(0,pos) + "_tagged.txt");
            this.pw = new PrintWriter(fichero);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void writeFile(String texto) {
        pw.print(texto);
    }

    public void nextLineFile() {
        pw.println();
    }

    public void closeLastFile() {
        try {
            if (null != fichero) {
                fichero.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
