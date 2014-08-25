//
//  ViewController.m
//  SocketSample
//
//  Created by ishimaru on 2014/08/25.
//  Copyright (c) 2014年 mrk1869. All rights reserved.
//

#import "ViewController.h"
#import "SRWebSocket.h"

@interface ViewController ()<SRWebSocketDelegate, UITextFieldDelegate>{
    SRWebSocket *client;
    BOOL canSendMessage;
}

@end

@implementation ViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    NSURLRequest *request = [[NSURLRequest alloc] initWithURL:[NSURL URLWithString:@"http://localhost:8000/socket"]];
    client = [[SRWebSocket alloc] initWithURLRequest:request];
    client.delegate = self;
    [client open];
    
    self.messageSendingTextField.delegate = self;
    self.messageSendingTextField.returnKeyType = UIReturnKeyDone;
}

-(void)webSocketDidOpen:(SRWebSocket *)webSocket
{
    NSLog(@"Websocket Connected");
    canSendMessage = YES;
}

- (void)webSocket:(SRWebSocket *)webSocket didReceiveMessage:(id)message
{
    self.resultTextView.text = [NSString stringWithFormat:@"%@\n%@",message,self.resultTextView.text];
}

-(void)webSocket:(SRWebSocket *)webSocket didCloseWithCode:(NSInteger)code reason:(NSString *)reason wasClean:(BOOL)wasClean
{
    NSLog(@"WebSocket closed");
    canSendMessage = NO;
    client = nil;
}

- (void)webSocket:(SRWebSocket *)webSocket didFailWithError:(NSError *)error
{
    NSLog(@"Websocket Failed With Error: %@", error);
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField
{
    [textField resignFirstResponder];
    if (!canSendMessage) {
        return YES;
    }
    NSString *message = textField.text;
    textField.text = @"";
    [client send:message];
    return YES;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
