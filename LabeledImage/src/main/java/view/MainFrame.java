package view;

import java.awt.Image;
import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import java.awt.event.KeyEvent;
import utils.Utils;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.Scanner;

public class MainFrame extends javax.swing.JFrame {

    private final String path = "/Users/ignacio/TFG/TFG/data/LPATrail20-Salida_faces_prueba";
    private File[] files;
    private Utils utils;
    int width = 1920;
    int height = 1080;
    int positionImage = 0;
    private double factorScale = 1.3;
    private int control = 0;
    
    public MainFrame() {
        initComponents();
        setFocusable(true);
        setSize(1850, 1200);
        listFiles();
        printImage(0);
        this.utils = new Utils(files[positionImage].getName(), path);
        CerrarVentana();
    }

   
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        titleImage = new javax.swing.JLabel();
        image = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        screen = new javax.swing.JTextArea();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                formMouseClicked(evt);
            }
        });
        addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                formKeyPressed(evt);
            }
        });

        titleImage.setText("Title");

        screen.setColumns(20);
        screen.setRows(5);
        jScrollPane1.setViewportView(screen);

        org.jdesktop.layout.GroupLayout layout = new org.jdesktop.layout.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
                    .add(layout.createSequentialGroup()
                        .add(174, 174, 174)
                        .add(titleImage, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                    .add(layout.createSequentialGroup()
                        .add(164, 164, 164)
                        .add(image)))
                .add(201, 201, 201))
            .add(org.jdesktop.layout.GroupLayout.TRAILING, layout.createSequentialGroup()
                .add(17, 17, 17)
                .add(jScrollPane1)
                .add(24, 24, 24))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(layout.createSequentialGroup()
                .add(18, 18, 18)
                .add(titleImage)
                .add(28, 28, 28)
                .add(image)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 158, Short.MAX_VALUE)
                .add(jScrollPane1, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 67, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(14, 14, 14))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void formMouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMouseClicked
        if(control == 0){
            int x = evt.getX() - image.getLocation().x;
            int y = evt.getY() - image.getLocation().y - 25;
            int xWithOutScaled = (int) (factorScale  * x);
            int yWithOutScaled = (int) (factorScale * y);
            utils.writeFile(xWithOutScaled + " " + yWithOutScaled + " ");
            screen.append(xWithOutScaled + " " + yWithOutScaled + " ");
            control++;
        }
    }//GEN-LAST:event_formMouseClicked

    private void formKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_formKeyPressed
        if(evt.getKeyCode()==KeyEvent.VK_N && control == 0){
            if(positionImage < files.length - 1){
                positionImage++;
                printImage(positionImage);
                utils.changeFile(files[positionImage].getName());
                screen.append("\n=============================== Siguiente Fichero ===============================\n");
            } else{
                javax.swing.JOptionPane.showMessageDialog(this,"Completado el etiquetado de todas las imágenes","Mensaje",javax.swing.JOptionPane.ERROR_MESSAGE);
            }
        } 
        if (evt.getKeyCode()==KeyEvent.VK_S && control == 1){
            utils.writeFile("1 ");
            screen.append("1 ");
            control++;
        }
        if (evt.getKeyCode()==KeyEvent.VK_A && control == 1){
            utils.writeFile("0 ");
            screen.append("0 ");
            control++;
        }
        if (evt.getKeyCode() >= 48 && evt.getKeyCode() <= 57 && control == 2){    
            utils.writeFile(""+evt.getKeyChar());
            screen.append(""+evt.getKeyChar());          
        }
        if(evt.getKeyCode()==KeyEvent.VK_ENTER && control == 2){
            control = 0;
            utils.writeFile("\n");
            screen.append("\n");
        }
    }//GEN-LAST:event_formKeyPressed

    private void listFiles() {
        File dir = new File(this.path);
        files = dir.listFiles(new Filter());
    }

    private void printImage(int positionImage) {
        java.awt.image.BufferedImage image = null;
        File file = files[positionImage];
        try{
            image = ImageIO.read(file); 
        }catch(IOException ie){
            javax.swing.JOptionPane.showMessageDialog(this,"Error reading image file","Error",javax.swing.JOptionPane.ERROR_MESSAGE);
        }
        int widthScaled = (int) (width / factorScale);
        int heightScaled = (int) (height / factorScale);
        Image img = image.getScaledInstance(widthScaled,heightScaled,java.awt.Image.SCALE_SMOOTH);
        ImageIcon newIcon = new ImageIcon(img);
        String pictureName = file.getName();
        int pos = pictureName.lastIndexOf(".");  
        String caption = pictureName.substring(0,pos);
        this.image.setIcon(newIcon);                   
        titleImage.setText(positionImage + " " + caption);                      
    }
    
    private class Filter implements FilenameFilter{
        @Override
        public boolean accept(File dir, String name) {
            return name.toLowerCase().endsWith(".jpg");
        }       
    }
    
    public void CerrarVentana(){
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                utils.closeLastFile();
                System.exit(0);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel image;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JTextArea screen;
    private javax.swing.JLabel titleImage;
    // End of variables declaration//GEN-END:variables

}
