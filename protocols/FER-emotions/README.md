# Facial Expressions Recognition - Emotions

## Data collect

1. Explain the research and ask to the volunteer to sign the **Termo de Consentimento Livre e Esclarecido** (in english, Consent Form Free and Informed).

2. The volunteer will be positioned facing a webcam [Logitech C920](https://www.logitech.com/pt-br/product/hd-pro-webcam-c920).

3. Inform the facial expression to be played.
    * Repeat 3x

4. Provide examples (of [well-established bases](dataset-display/options.json)) of the facial expressions proposed.
    * Repeat 3x
    * [```display.py```](dataset-display/display.py)

## Data label

### Discard when capturing images:

1. Volunteers who have failed to remove any item that may cause occlusion should be discarded.
    * Beard
    * Tattoos
    * etc.

### After collection:

1. Determine the FACS codes for each image at the peak of emotion using the FACS manual [1, 2, 3]. If a sequence meets the criteria for an emotion, it will be provisionally coded as belonging to that category of emotion, otherwise discarded.

2. If a sequence includes an AU not included in the prototypes or variants, it will be determined whether this AU is consistent with the respective emotion or not. If it is considered inconsistent, the sequence will be discarded.

3. Perform a visual inspection of the remaining sequences to see if the expression really is a good representation for that category of emotion.
    * This stage will probably be performed with volunteers who did not participate in data collection.
    
4. The remaining sequences will be properly labeled among the categories: Anger, Disgust, Fear, Happy, Neutral, Sad and Surprise.

---
[1] Lucey, P., Cohn, J. F., Kanade, T., Saragih, J., Ambadar, Z., & Matthews, I. (2010). The Extended Cohn-Kanade Dataset (CK+): A complete dataset for action unit and emotion-specified expression. In 2010 IEEE Computer Society Conference on Computer Vision and Pattern Recognition - Workshops (pp. 94–101). IEEE. [https://doi.org/10.1109/CVPRW.2010.5543262](https://doi.org/10.1109/CVPRW.2010.5543262)

[2] Cohn, J. F., Ambadar, Z., & Ekman, P. (2007). Observer-based measurement of facial expression with the Facial Action Coding System. The Handbook of Emotion Elicitation and Assessment, 203–221.

[3] Ekman, P., & Rosenberg, E. L. (1997). What the face reveals: Basic and applied studies of spontaneous expression using the Facial Action Coding System (FACS). Oxford University Press, USA.
