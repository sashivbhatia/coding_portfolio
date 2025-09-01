//Sashiv Bhatia
//May 31st, 2023
//CSE 123
//Abosh Upadhyaya
//HuffmanCode

import java.util.*;
import java.io.*;

//This class creates a huffman code and can be used to compress and decompress binary files
public class HuffmanCode {

    //This private class creates a node for the huffman code class
    private static class HuffmanNode implements Comparable<HuffmanNode>{
        private char ch;
        private int freq;
        private HuffmanNode left;
        private HuffmanNode right;

        //Creates a HuffmanNode with a given character and a frequency
        private HuffmanNode(char ch, int freq){
            this.ch=ch;
            this.freq=freq;
        }

        //Creates a HuffmanNode with a frequency, a left and a right linked HuffmanNode
        private HuffmanNode(int freq, HuffmanNode left, HuffmanNode right){
            this.freq=freq;
            this.left=left;
            this.right=right;
        }

        //Returns 0, a positive or a negative number if the frequency of this HuffmanNode is 
        //equal, greater or less than frequency of other node
        @Override public int compareTo(HuffmanNode other){
            return this.freq-other.freq;
        }
    }

    private HuffmanNode root;

    //Creates a new HuffmanCode with a given array of counts. Each index in the array represents
    //the ASCII value and the number represents it's frequency.
    //Parameter: array of frequencies of characters
    public HuffmanCode(int[] count){
        Queue<HuffmanNode> pq = new PriorityQueue<>();
        for(int i = 0; i<count.length; i++){
            if(count[i]>0){
                pq.add(new HuffmanNode((char)i,count[i]));
            }
        }
        while(pq.size()>1){
            HuffmanNode temp1 = pq.remove();
            HuffmanNode temp2 = pq.remove();
            HuffmanNode moo = new HuffmanNode(temp1.freq + temp2.freq, temp1, temp2);
            pq.add(moo);
        }

        this.root = pq.remove();
    }

    //Creates a new HuffmanCode with a given scanned file. Each pair of lines represents
    //an ascii code in the first line followed by it's path in the tree in the next line
    //Parameter: array of frequencies of characters
    public HuffmanCode(Scanner input) {
        while (input.hasNextLine()) {
            char ch = (char)Integer.parseInt(input.nextLine());
            String path = input.nextLine();
            this.root = createHuffman(ch, path, this.root);
        }
    }

    //Private helper method for HuffmanCode(Scanner input)
    //This method traverses through the current root until it reaches a leaf node, 
    //creating new HuffmanNodes on the way if they didn't exist, and adding
    //the character to the leaf node
    //Parameters: char to add, the path to follow and the current HuffmanNode
    //Returns the node with added char
    private HuffmanNode createHuffman(char ch, String path, HuffmanNode node){
        if (path.isEmpty()) {
            return new HuffmanNode(ch, 0);
        }
        if(node == null){
            node = new HuffmanNode((char)0,0);
        }
        if (path.charAt(0) == '0') {
            node.left = createHuffman(ch, path.substring(1), node.left);
        } else {
            node.right = createHuffman(ch, path.substring(1), node.right);
        }
              
        return node;
    }

    //Writes the current Huffman codes to a given output PrintStream where in each pair of lines
    //the first line contains the ASCII value of the character and the second line contains
    //the path to the character
    //Parameter: the output PrintStream
    public void save(PrintStream output){
        String str = "";
        save(output, str, this.root);
    }

    //Private helper method for save(PrintStream output) method
    //Creates a path to the leaf nodes and prints to the PrintStream output when the 
    //leaf is reached
    //Parameters: the output PrintStream, the string to maintain path to the leaf and the current HuffmanNode
    private void save(PrintStream output, String str, HuffmanNode node){
        if((int)node.ch!=0){
            output.println((int)node.ch);
            output.println(str);
        }
        else{
            save(output, str+"0",node.left);
            save(output, str+"1",node.right);
        }
    }

    //Reads bits of information from the input, translates it into characters and prints them into the output PrintStream
    //Parameters: the BitInputStream input containing bits of information and the output PrintStream
    public void translate(BitInputStream input, PrintStream output){
        while(input.hasNextBit()){
            translate(this.root, input, output);
        }
    }

    //Private helper method for translate(BitInputStream input, PrintStream output)
    //The method traverses the HuffmanCode tree until a leaf is reached and then 
    //outputs the character in the leaf onto the PrintStream output once it is reached.
    //Parameters: the current HuffmanNode, the input BitInputStream and the output PrintStream
    private void translate(HuffmanNode node, BitInputStream input, PrintStream output){
        if(node.left == null && node.right == null){
            output.write(node.ch);
        }
        else{
            int temp = input.nextBit();
            if(temp==0){
                translate(node.left, input, output);
            }
            else{
                translate(node.right, input, output);
            }
        }
    }
}
