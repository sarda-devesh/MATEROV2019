package com.example.rov2019app;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    Spinner spin1;
    Spinner spin2;
    Spinner spin3;
    Spinner spin4;
    EditText quadl;
    EditText quadw;
    EditText musl;
    EditText musw;
    EditText filter;
    EditText counter;
    TextView display;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        setup();
        updateDropdown(spin1);
        updateDropdown(spin2);
        updateDropdown(spin3);
        updateDropdown(spin4);
        Button enter = (Button) findViewById(R.id.enter);

        enter.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                double bigarea = getInformation(musl, spin3) * getInformation(musw, spin4);
                double smallarea = getInformation(quadl, spin1) * getInformation(quadw, spin2);
                int found = Integer.parseInt(counter.getText().toString());
                double filternation = Double.parseDouble(filter.getText().toString());
                double total = filternation * found * (bigarea/smallarea);
                total = Math.round(total * 1000)/1000.0;
                String output = "There is a total of " + total + " mussles in the bed";
                display.setText(output);
            }
        });

    }

    private void setup() {
        spin1 = (Spinner) findViewById(R.id.squadl);
        spin2 = (Spinner) findViewById(R.id.squadw);
        spin3 = (Spinner) findViewById(R.id.smusl);
        spin4 = (Spinner) findViewById(R.id.smusw);
        quadl = (EditText) findViewById(R.id.quadl);
        quadw = (EditText) findViewById(R.id.quadw);
        musl = (EditText) findViewById(R.id.musl);
        musw = (EditText) findViewById(R.id.musw);
        filter = (EditText) findViewById(R.id.filter);
        counter = (EditText) findViewById(R.id.counter);
        display = (TextView) findViewById(R.id.output);
    }

    private void updateDropdown(Spinner current) {
        String[] items = new String[]{"m    ", "cm     "};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, items);
        current.setAdapter(adapter);
    }

    private double getInformation(EditText value, Spinner current) {
        double dimension = 1.0  * Integer.parseInt(value.getText().toString());
        if(current.getSelectedItem().toString().contains("cm")) {
            dimension /= 100;
        }
        return dimension;
    }



}