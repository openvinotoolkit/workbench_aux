import { Injectable } from '@angular/core';

import messages from '../../../assets/data/messages.json';

@Injectable({
  providedIn: 'root'
})
export class MessagesService {
  public static readonly messages = messages;
  public readonly messages = MessagesService.messages;
}
