package utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

public class Utils {

    private FileWriter fileWrite;
    private PrintWriter pw;
    private String path;
    private String nameFile;
    private FileReader fr;
    private File fileRead;
    private BufferedReader br;

    public Utils(String nameFile, String path) {
        this.path = path;
        this.nameFile = nameFile;
    }

    public boolean changeFileRead(String nameFile) {
        int pos = nameFile.lastIndexOf(".");
        try {
            if (null != fr) {
                fr.close();
            }
        } catch (Exception e2) {
            e2.printStackTrace();
        }
        fileRead = new File(this.path + "/" + nameFile.substring(0, pos) + "_faces.txt");
        if(fileRead.exists()){
            try {
                fr = new FileReader(fileRead);
            } catch (FileNotFoundException ex) {
                ex.printStackTrace();
            }
            br = new BufferedReader(fr);
            return true;
        } else{
            return false;
        }
    }

    public void changeFileWrite(String nameFile) {
        int pos = nameFile.lastIndexOf(".");
        try {
            if (null != fileWrite) {
                fileWrite.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            this.fileWrite = new FileWriter(this.path + "/" + nameFile.substring(0, pos) + "_tagged.txt");
            this.pw = new PrintWriter(fileWrite);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void writeFile(String texto) {
        pw.print(texto);
    }

    public ArrayList<String> readAllFile() {
        ArrayList<String> listLine = new ArrayList<String>();
        try {
            String line;
            while ((line = br.readLine()) != null) {
                listLine.add(line);
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        return listLine;
    }

    public void nextLineFile() {
        pw.println();
    }

    public void closeLastFileWrite() {
        try {
            if (null != fileWrite) {
                fileWrite.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void closeLastFileRead() {
        try {
            if (null != fr) {
                fr.close();
            }
        } catch (Exception e2) {
            e2.printStackTrace();
        }
    }
    
    public void printBox(String[] words){
        
    }
}
