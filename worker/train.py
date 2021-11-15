from tqdm import tqdm
from utils.compute_avg import *
import torch
import copy


class BaseTrainer:

    def __init__(self, tasks=None):

        self.task = tasks
        self.best = None


    async def __aenter__(self, model, loaders, criterion, optimizer, history, model_params, opt, device):

        his, self.best = self.phase(model, loaders, criterion, optimizer, history, model_params, opt, device)


        return his

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        pass

    def phase(self, model, loaders, criterion, optimizer, history, model_params, opt, device):

        model.load_state_dict(copy.deepcopy(history['params']), strict=False)
        train_loader, val_loader = loaders

        train_loss, train_acc = self.train_epoch(model, train_loader, criterion, optimizer, history['epoch'],
                                            opt.log_interval, device)
        history['train_los'].append(train_loss), history['train_acc'].append(train_acc)

        val_loss, val_acc = self.val_epoch(model, val_loader, criterion, device)
        history['val_los'].append(val_loss), history['val_acc'].append(val_acc)

        history['params'] = copy.deepcopy(model.state_dict())
        history['epoch'] += 1

        if val_loss < model_params['best_loss']:
            model_params['best_loss'] = val_loss
            model_params['best_params'] = copy.deepcopy(model.state_dict())

        return history, model_params

    def train_epoch(self, model, data_loader, criterion, optimizer, epoch, log_interval, device):

        model.train()
        train_loss = 0.0
        losses = ComputeAvg()
        accuracies = ComputeAvg()
        batch_idx = 0

        for (data, targets) in tqdm(data_loader, desc='Train ::'):
            data, targets = data.to(device), targets.to(device)
            outputs = model(data)
            loss = criterion(outputs, targets)
            acc = calculate_acc(outputs, targets)

            train_loss += loss.item()
            losses.update(loss.item(), data.size(0))
            accuracies.update(acc, data.size(0))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (batch_idx + 1) % log_interval == 0:
                avg_loss = train_loss / log_interval
                print(f' log e[{epoch}]: [{(batch_idx + 1) * len(data)}/{len(data_loader.dataset)} ({((batch_idx + 1)/len(data_loader))*100.0:.0f}%)]\tLoss: {avg_loss:.6f}'
                    )
                train_loss = 0.0

            batch_idx += 1


        print(f"Train Done ({len(data_loader.dataset)}"
              f" samples): Average loss: {losses.avg:.4f}\t"
              f"Acc: {(accuracies.avg*100):.4f}%")

        return losses.avg, accuracies.avg

    def val_epoch(self, model, data_loader, criterion, device):
        model.eval()
        print(f'val start', end=': ')
        losses = ComputeAvg()
        accuracies = ComputeAvg()
        with torch.no_grad():
            for (data, targets) in tqdm(data_loader, desc='val epoch:: '):
                data, targets = data.to(device), targets.to(device)
                outputs = model(data)

                loss = criterion(outputs, targets)
                acc = calculate_acc(outputs, targets)

                losses.update(loss.item(), data.size(0))
                accuracies.update(acc, data.size(0))
                # print('epoch')
        # show info

        print(f"Validation Done ({len(data_loader.dataset)}"
              f" samples): Average loss: {losses.avg:.4f}\t"
              f"Acc: {(accuracies.avg * 100):.4f}%")

        return losses.avg, accuracies.avg