//Sashiv Bhatia
//May 10th, 2023
//CSE 123
//Abosh Upadhyaya
//Mondrian
import java.util.*;
import java.awt.*;

//This class creates an image that attempts to evoke the art of Mondrian
public class Mondrian {

//This method adds a border to the canvas and calls the method that creates 
//a basic mondrian art image
//One parameter: 2d array that is the blank canvas
//No return variable
    public void paintBasicMondrian(Color[][] pixels){
        subdivide(pixels,1,pixels.length-1,1,pixels[0].length-1);
    }

//This method checks whether the lenth and width of the current rectangle 
//is more than 1/4 of the canvas' length and width
//If both are more, it subdivides the rectangle into 4 smaller rectangles at
//a random width and height and calls the subdivide method on each
//If only one is more, it subdivides the rectangle into 2 smaller rectangles at
//a random height/width respectively and calls the subdivide method on each
//If both are smaller, it calls the fill color method on that rectangle
//It takes five parameters: the canvas and the min/max height and width of the rectangle
    private void subdivide(Color[][] pixels, int minHeight, int maxHeight, int minWidth, 
    int maxWidth){
        int newHeight = (int)(Math.random()*(maxHeight-minHeight)+1);
        int newWidth = (int)(Math.random()*(maxWidth-minWidth)+1);
        if(pixels.length/4<=(maxHeight-minHeight) && pixels[0].length/4<(maxWidth-minWidth)){
            subdivide(pixels,minHeight,newHeight+minHeight,minWidth,newWidth+minWidth);
            subdivide(pixels,newHeight+minHeight,maxHeight,minWidth,newWidth+minWidth);
            subdivide(pixels,minHeight,newHeight+minHeight,newWidth+minWidth,maxWidth);
            subdivide(pixels,newHeight+minHeight,maxHeight,newWidth+minWidth,maxWidth);
        }
        else if(pixels.length/4<=(maxHeight-minHeight)){
            subdivide(pixels,minHeight,newHeight+minHeight,minWidth,maxWidth);
            subdivide(pixels,newHeight+minHeight,maxHeight,minWidth,maxWidth);
        }
        else if(pixels[0].length/4<=(maxWidth-minWidth)){
            subdivide(pixels,minHeight,maxHeight,minWidth,newWidth+minWidth);
            subdivide(pixels,minHeight,maxHeight,newWidth+minWidth,maxWidth);
        }
        else{
            fillColor(minHeight+1, maxHeight-1, minWidth+1, maxWidth-1, pixels);
        }
    }

//This method fills a rectangle on the canvas with a 
//random color between red, cyan, yellow and WHITE
//It takes five parameters: the canvas and the min/max height and width of the rectangle
    private void fillColor(int h0, int h1, int w0, int w1,Color[][] pixels){
        int temp = (int)(Math.random()*(4)+1);
        for(int i = h0; i<h1; i++){
            for(int j = w0; j<w1; j++){
                if(temp==1){
                    pixels[i][j]=Color.RED;
                }
                else if(temp==2){
                    pixels[i][j]=Color.YELLOW;
                }
                else if(temp==3){
                    pixels[i][j]=Color.CYAN;
                }
                else if(temp==4){
                    pixels[i][j]=Color.WHITE;
                }
            }
        }
    }

//EXTENSION!!

//This method adds a border to the canvas and calls the method 
//that creates a basic mondrian art image
//One parameter: 2d array that is the blank canvas
//No return variable
    public void paintComplexMondrian(Color[][] pixels){
        subdivideComplex(pixels,1,pixels.length-1,1,pixels[0].length-1);
    }

//This method checks whether the lenth and width of the current rectangle is 
//more than 1/4 of the canvas' length and width
//If both are more, it subdivides the rectangle into 4 smaller rectangles at
//a random width and height and calls the subdivide method on each
//If only one is more, it subdivides the rectangle into 2 smaller rectangles at
//a random height/width respectively and calls the subdivide method on each
//If both are smaller, it calls the complex fill color method on that rectangle
//It takes five parameters: the canvas and the min/max height and width of the rectangle
    private void subdivideComplex(Color[][] pixels, int minHeight, int maxHeight, int minWidth,
    int maxWidth){
        int newHeight = (int)(Math.random()*(maxHeight-minHeight)+1);
        int newWidth = (int)(Math.random()*(maxWidth-minWidth)+1);
        if(pixels.length/4<=(maxHeight-minHeight) && pixels[0].length/4<(maxWidth-minWidth)){
            subdivideComplex(pixels,minHeight,newHeight+minHeight,minWidth,newWidth+minWidth);
            subdivideComplex(pixels,newHeight+minHeight,maxHeight,minWidth,newWidth+minWidth);
            subdivideComplex(pixels,minHeight,newHeight+minHeight,newWidth+minWidth,maxWidth);
            subdivideComplex(pixels,newHeight+minHeight,maxHeight,newWidth+minWidth,maxWidth);
        }
        else if(pixels.length/4<=(maxHeight-minHeight)){
            subdivideComplex(pixels,minHeight,newHeight+minHeight,minWidth,maxWidth);
            subdivideComplex(pixels,newHeight+minHeight,maxHeight,minWidth,maxWidth);
        }
        else if(pixels[0].length/4<=(maxWidth-minWidth)){
            subdivideComplex(pixels,minHeight,maxHeight,minWidth,newWidth+minWidth);
            subdivideComplex(pixels,minHeight,maxHeight,newWidth+minWidth,maxWidth);
        }
        else{
            fillColorComplex(minHeight+1, maxHeight-1, minWidth+1, maxWidth-1, pixels);
        }
    }

//This method fills a rectangle on the canvas with a random color 
//between red, cyan, yellow and white 
//If the rectangle is in the top right, it is more likely to be cyan in color.
//Similarly, red if it is in the bottom right, yellow if it is in the bottom
//left and white if in the top left
//It takes five parameters: the canvas and the min/max height and width of the rectangle
    private void fillColorComplex(int h0, int h1, int w0, int w1,Color[][] pixels){
        Color[] q1 = {Color.CYAN,Color.CYAN,Color.CYAN,Color.CYAN,Color.CYAN,Color.CYAN,
            Color.RED,Color.YELLOW,Color.WHITE};
        Color[] q2 = {Color.CYAN, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED,
            Color.YELLOW,Color.WHITE};
        Color[] q3 = {Color.CYAN, Color.RED, Color.YELLOW, Color.YELLOW, Color.YELLOW,
            Color.YELLOW, Color.YELLOW, Color.YELLOW, Color.WHITE};
        Color[] q4 = {Color.CYAN, Color.RED, Color.YELLOW,Color.WHITE, Color.WHITE, Color.WHITE,
            Color.WHITE,Color.WHITE,Color.WHITE};

        int temp = (int)(Math.random()*(6));
        int midHeight = pixels.length/2;
        int midWidth = pixels[0].length/2;

        if((h1+h0)/2<=midHeight && (w1+w0)/2<=midWidth){
            for(int i = h0 ; i<h1; i++){
                for(int j = w0 ; j<w1; j++){
                    pixels[i][j]=q3[temp];
                }
            }
        }

        else if((h1+h0)/2>=midHeight && (w1+w0)/2<=midWidth){
            for(int i = h0 ; i<h1; i++){
                for(int j = w0 ; j<w1; j++){
                    pixels[i][j]=q4[temp];
                }
            }
        }

        else if((h1+h0)/2>=midHeight && (w1+w0)/2>=midWidth){
            for(int i = h0 ; i<h1; i++){
                for(int j = w0 ; j<w1; j++){
                    pixels[i][j]=q1[temp];
                }
            }
        }
        else{
            for(int i = h0 ; i<h1; i++){
                for(int j = w0 ; j<w1; j++){
                    pixels[i][j]=q2[temp];
                }
            }
        }
    }
}
