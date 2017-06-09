### red dice from PALs Maps ###

from wx import ImageFromStream, BitmapFromImage, EmptyIcon
from wx.lib.embeddedimage import PyEmbeddedImage
import cStringIO

#----------------------------------------------------------------------
small_red_dice = PyEmbeddedImage(
    "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")
getsmall_red_diceData = small_red_dice.GetData
getsmall_red_diceImage = small_red_dice.GetImage
getsmall_red_diceBitmap = small_red_dice.GetBitmap

