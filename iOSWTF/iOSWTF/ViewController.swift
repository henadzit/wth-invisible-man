//
//  ViewController.swift
//  iOSWTF
//
//  Created by Anthony Marchenko on 11/24/17.
//  Copyright © 2017 Anthony Marchenko. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var versionLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        versionLabel.text = OpenCVWrapper.openCVVersion()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

