# coding: UTF-8
import os
import os.path as osp
import shutil

import torch
import numpy as np

from torchtools.callbacks.callback import Callback


class ModelCheckPoint(Callback):
    def __init__(self, save_dir=None,
                 fname='{arch}_{epochs:05d}_{val_loss:.2f}.pt',
                 monitor='val_loss', mode='auto', period=1,
                 save_best_only=True):
        if not save_dir:
            save_dir = 'checkpoints'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.save_dir = save_dir
        self.fname = fname
        self.fpath = osp.join(save_dir, fname)
        self.monitor = monitor
        self.period = period
        self.epochs_since_last_saved = 0
        self.save_best_only = save_best_only
        if mode == 'min':
            self.monitor_op = np.less
            self.best = np.inf
        elif mode == 'max':
            self.monitor_op = np.greater
            self.best = -np.inf
        else:
            if 'acc' in self.monitor:
                self.monitor_op = np.greater
                self.best = -np.inf
            else:
                self.monitor_op = np.less
                self.best = np.inf

    def on_epoch_end(self, trainer, state):
        self.epochs_since_last_saved += 1
        if self.epochs_since_last_saved < self.period:
            return
        self.epochs_since_last_saved = 0

        val = state['meters'][self.monitor].value
        path_vals = state
        path_vals[self.monitor] = val
        fpath = self.fpath.format(**path_vals)
        checkpoint = {
            'epochs': state['epochs'],
            'iters': state['iters'],
            'model_state_dict': state['model'].state_dict(),
            'optimizer_state_dict': state['optimizer'].state_dict(),
        }
        if not self.save_best_only:
            torch.save(checkpoint, fpath)

        if self.monitor_op(val, self.best):
            self.best = val
            best_fpath = osp.join(self.save_dir, 'best_' + self.fname).format(
                **path_vals)
            if not self.save_best_only:
                shutil.copy(fpath, best_fpath)
            else:
                torch.save(checkpoint, best_fpath)
